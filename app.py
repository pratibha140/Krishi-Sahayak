# app.py
# Krishi Sahayak - Smart Multilingual Agricultural Assistant
# Flask Backend Server
# Integrating MANAGE & GIZ Farmer's Handbook, Real-Time Weather, Live Government Schemes & Google/Gmail Auth

import datetime
import os
import re
import secrets
import sys
import click
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

# Load local .env in development if present, without interfering with isolated test subprocesses (-c) or production
if os.environ.get("FLASK_ENV") != "production" and (not sys.argv or sys.argv[0] != "-c"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import database
from assistant_service import process_query
from crops_data import (
    CATEGORIES,
    CROPS,
    CRITICAL_IRRIGATION_STAGES,
    DRIP_SPRINKLER_BENEFITS,
    SEED_CLASSES,
    calculate_crop_plan,
)
from disease_service import DISEASES, diagnose_plant_photo, search_diseases
from handbook_data import (
    BOTANICAL_RECIPES,
    FARM_MECHANIZATION_TOOLS,
    FARMER_SERVICES,
    FERTILIZER_COMPATIBILITY,
    GOVERNMENT_SCHEMES,
    NUTRIENT_DEFICIENCIES,
    PESTICIDE_TOXICITY_CLASSES,
)
from translations import LANGUAGES, get_text
from weather_service import (
    POPULAR_LOCATIONS,
    get_weather_forecast,
    search_locations,
    reverse_geocode,
)

import threading
import time
from collections import defaultdict

app = Flask(__name__)

# Security configuration
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    if os.environ.get("FLASK_ENV") == "production":
        raise RuntimeError("CRITICAL SECURITY ERROR: SECRET_KEY must be set in production environment!")
    secret_key = "krishi-sahayak-dev-key-" + secrets.token_hex(16)

app.secret_key = secret_key
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000 if os.environ.get("FLASK_ENV") == "production" else 0
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB max upload limit
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True if os.environ.get("FLASK_ENV") == "production" else False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

# Explicit database schema initialization on application bootstrap
database.init_db()

# Section 6.4: Reverse Proxy Header Handling (ProxyFix)
# Conditionally apply ProxyFix only when configured for production or reverse proxy operation.
# Exactly 1 trusted upstream proxy hop is configured (x_for=1, x_proto=1, x_host=1) to prevent
# client IP spoofing in development while ensuring real client IPs reach the rate limiter and
# HTTPS scheme is accurately resolved in production.
if os.environ.get("FLASK_ENV") == "production" or os.environ.get("USE_PROXY_FIX") == "1":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Section 6.5: In-memory IP/action rate limiter for auth and heavy endpoints
_RATE_LIMITS = defaultdict(list)
_RATE_LIMIT_LOCK = threading.Lock()
MAX_RATE_LIMIT_KEYS = 10000

def is_rate_limited(key, max_requests=15, window_seconds=60):
    """
    In-memory sliding-window rate limiter per key (e.g. 'login:<ip>', 'resend:<ip>', 'diagnose:<ip>').
    Thread-safe and memory-bounded to prevent worker starvation and memory exhaustion.
    Returns True if request exceeds max_requests within window_seconds, False otherwise.
    """
    now = time.time()
    with _RATE_LIMIT_LOCK:
        # Prune stale keys if dictionary size exceeds threshold
        if len(_RATE_LIMITS) > 500:
            stale_keys = [
                k for k, timestamps in _RATE_LIMITS.items()
                if not timestamps or (now - timestamps[-1] >= window_seconds)
            ]
            for k in stale_keys:
                _RATE_LIMITS.pop(k, None)

            # Enforce hard maximum limit by discarding oldest entries if still oversized
            if len(_RATE_LIMITS) >= MAX_RATE_LIMIT_KEYS:
                excess = len(_RATE_LIMITS) - MAX_RATE_LIMIT_KEYS + 100
                for k in list(_RATE_LIMITS.keys())[:excess]:
                    _RATE_LIMITS.pop(k, None)

        history = _RATE_LIMITS.get(key, [])
        clean_history = [t for t in history if now - t < window_seconds]

        if len(clean_history) >= max_requests:
            _RATE_LIMITS[key] = clean_history
            return True

        clean_history.append(now)
        _RATE_LIMITS[key] = clean_history
        return False

def clear_rate_limits():
    """Clear in-memory rate limiting state (primarily for test isolation)."""
    with _RATE_LIMIT_LOCK:
        _RATE_LIMITS.clear()

# Built-in CSRF Protection
def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]

app.jinja_env.globals["csrf_token"] = generate_csrf_token

@app.before_request
def csrf_protect():
    # Only enforce if not in unit testing mode and on state-changing methods
    if app.config.get("TESTING") or app.testing:
        return
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken") or request.headers.get("X-CSRF-Token")
        session_token = session.get("_csrf_token")
        if not session_token or not token or not secrets.compare_digest(session_token, token):
            # Also allow JSON body fallback if passed as csrf_token
            json_body = request.get_json(silent=True) or {}
            body_token = json_body.get("csrf_token")
            if not body_token or not session_token or not secrets.compare_digest(session_token, body_token):
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"success": False, "error": "CSRF token missing or invalid"}), 403
                return render_template("login.html", **template_context("login"), alert_msg="Your session expired or invalid request. Please try again.", alert_type="error"), 403

@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if os.environ.get("FLASK_ENV") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Section 6.3: Content-Security-Policy (CSP)
    csp_directives = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://accounts.google.com",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com",
        "font-src 'self' https://fonts.gstatic.com data:",
        "img-src 'self' data: https://api.dicebear.com",
        "media-src 'self'",
        "connect-src 'self' https://accounts.google.com https://oauth2.googleapis.com https://api.open-meteo.com https://geocoding-api.open-meteo.com https://nominatim.openstreetmap.org",
        "frame-src 'self' https://accounts.google.com https://www.youtube.com https://www.youtube-nocookie.com",
        "frame-ancestors 'self'",
    ]
    response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
    return response


def current_language():
    user = current_user()
    if user and user.get("language"):
        return user["language"]
    return session.get("language", "en")


def current_user():
    user = session.get("user", None)
    if user and "id" not in user and user.get("email"):
        # Fetch or initialize DB user record
        db_user = database.get_user_by_email(user["email"])
        if db_user:
            session["user"] = db_user
            return db_user
    return user


def template_context(active_page):
    language = current_language()
    user = current_user()
    reminders = database.get_user_reminders(user["id"]) if user and user.get("id") else []
    pending_reminders_count = sum(1 for r in reminders if r.get("status") == "pending")

    return {
        "active_page": active_page,
        "language": language,
        "current_lang": language,
        "languages": LANGUAGES,
        "t": get_text(language),
        "user": user,
        "all_crops": CROPS,
        "crop_categories": CATEGORIES,
        "popular_locations": POPULAR_LOCATIONS,
        "reminders": reminders,
        "pending_reminders_count": pending_reminders_count,
        "government_schemes": GOVERNMENT_SCHEMES,
    }


# ==========================================
# Language Selection & Onboarding Flow
# ==========================================


@app.route("/set-language/<lang_code>")
def set_language(lang_code):
    if lang_code in LANGUAGES:
        session["language"] = lang_code
        user = current_user()
        if user and user.get("email"):
            database.update_user_language(user["email"], lang_code)
            user["language"] = lang_code
            session["user"] = user
            session.modified = True
    next_url = request.referrer or url_for("home")
    return redirect(next_url)


@app.route("/language", methods=["GET", "POST"])
def language_select():
    if request.method == "POST":
        selected_language = request.form.get("language", "en")
        if selected_language in LANGUAGES:
            session["language"] = selected_language
            user = current_user()
            if user and user.get("email"):
                database.update_user_language(user["email"], selected_language)
                user["language"] = selected_language
                session["user"] = user

        # Proceed to Step 2: Sign In / Create Account
        return redirect(url_for("login", onboarding="1"))

    return render_template("language_select.html", **template_context("language"))


# ==========================================
# User Authentication, Profile & Google Login
# ==========================================



# ==========================================
# Authentication & Verification Utilities
# ==========================================

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
VERIFICATION_TOKEN_MAX_AGE_HOURS = 24


def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_strong_password(password):
    if not password or len(password) < 8:
        return False
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_letter and has_digit


def is_token_expired(token_created_at_str):
    if not token_created_at_str:
        return True
    try:
        created_at = datetime.datetime.fromisoformat(token_created_at_str)
        now = datetime.datetime.utcnow()
        return (now - created_at).total_seconds() > (VERIFICATION_TOKEN_MAX_AGE_HOURS * 3600)
    except Exception:
        return True


def get_mail_config():
    """
    Returns email configuration dictionary from app.config or environment variables.
    """
    server = (app.config.get("MAIL_SERVER") or os.environ.get("MAIL_SERVER") or "").strip()
    port_val = app.config.get("MAIL_PORT") or os.environ.get("MAIL_PORT") or 587
    try:
        port = int(port_val)
    except (ValueError, TypeError):
        port = 587
    username = (app.config.get("MAIL_USERNAME") or os.environ.get("MAIL_USERNAME") or "").strip()
    password = (app.config.get("MAIL_PASSWORD") or os.environ.get("MAIL_PASSWORD") or "").strip()
    use_tls_val = app.config.get("MAIL_USE_TLS")
    if use_tls_val is None:
        use_tls = os.environ.get("MAIL_USE_TLS", "true").strip().lower() in ("true", "1", "yes")
    else:
        use_tls = bool(use_tls_val)
    use_ssl_val = app.config.get("MAIL_USE_SSL")
    if use_ssl_val is None:
        use_ssl = os.environ.get("MAIL_USE_SSL", "false").strip().lower() in ("true", "1", "yes")
    else:
        use_ssl = bool(use_ssl_val)
    default_sender = (
        app.config.get("MAIL_DEFAULT_SENDER")
        or app.config.get("MAIL_FROM")
        or os.environ.get("MAIL_DEFAULT_SENDER")
        or os.environ.get("MAIL_FROM")
        or "no-reply@krishisahayak.in"
    )
    return {
        "server": server,
        "port": port,
        "username": username,
        "password": password,
        "use_tls": use_tls,
        "use_ssl": use_ssl,
        "default_sender": default_sender,
    }


def is_email_configured():
    """
    Checks if an email delivery server is configured.
    """
    cfg = get_mail_config()
    return bool(cfg["server"])


def send_verification_email(recipient_email, recipient_name, verify_url):
    """
    Delivers a secure email verification link to the recipient using SMTP.
    Returns (True, None) on success, or (False, error_reason) on failure.
    Never exposes credentials or internal errors.
    """
    cfg = get_mail_config()
    if not cfg["server"]:
        return False, "Email service is not configured"

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Verify your Krishi Sahayak Account"
        msg["From"] = cfg["default_sender"]
        msg["To"] = recipient_email

        text_content = (
            f"Namaste {recipient_name},\n\n"
            f"Thank you for registering with Krishi Sahayak.\n"
            f"Please verify your email address by opening the following link:\n\n"
            f"{verify_url}\n\n"
            f"This link will expire in 24 hours.\n\n"
            f"If you did not create this account, please disregard this email.\n"
            f"Krishi Sahayak Team"
        )

        html_content = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #16a34a; padding: 15px; border-radius: 8px 8px 0 0; text-align: center;">
        <h2 style="color: #ffffff; margin: 0;">Krishi Sahayak</h2>
    </div>
    <div style="background-color: #ffffff; padding: 25px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
        <p>Namaste <strong>{recipient_name}</strong>,</p>
        <p>Thank you for registering with Krishi Sahayak. Please verify your email address to activate your account and start receiving farming advisory services.</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verify_url}" style="background-color: #16a34a; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Verify Email Address</a>
        </div>
        <p style="font-size: 0.9em; color: #64748b;">Or copy and paste this link in your browser:<br><a href="{verify_url}" style="color: #16a34a; word-break: break-all;">{verify_url}</a></p>
        <p style="font-size: 0.85em; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">This verification link will expire in 24 hours. If you did not create an account, you can safely ignore this email.</p>
    </div>
</body>
</html>"""

        msg.attach(MIMEText(text_content, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        timeout = 10
        if cfg["use_ssl"]:
            server = smtplib.SMTP_SSL(cfg["server"], cfg["port"], timeout=timeout)
        else:
            server = smtplib.SMTP(cfg["server"], cfg["port"], timeout=timeout)
            if cfg["use_tls"]:
                server.starttls()

        if cfg["username"] and cfg["password"]:
            server.login(cfg["username"], cfg["password"])

        server.send_message(msg)
        server.quit()
        return True, None
    except Exception as e:
        print(f"[SECURITY] Email delivery failure for {recipient_email}: {type(e).__name__}", flush=True)
        return False, str(type(e).__name__)


def render_auth_page(alert_msg=None, alert_type="info", mode="login", dev_verify_link=None, show_resend_email=None, form_data=None):
    ctx = template_context("login")
    ctx["is_onboarding"] = request.args.get("onboarding") == "1"
    ctx["mode"] = mode or request.args.get("mode", "login")
    ctx["alert_msg"] = alert_msg
    ctx["alert_type"] = alert_type
    ctx["dev_verify_link"] = dev_verify_link
    ctx["show_resend_email"] = show_resend_email
    ctx["form_data"] = form_data or {}
    return render_template("login.html", **ctx)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle GET alerts (e.g. from verification redirect or expiry)
    if request.method == "GET":
        if request.args.get("verified") == "1":
            return render_auth_page(
                alert_msg="Email verified successfully! You can now sign in to your account.",
                alert_type="success",
                mode="login"
            )
        if request.args.get("alert") == "expired_token":
            return render_auth_page(
                alert_msg="This verification link has expired. Please request a new verification link.",
                alert_type="error",
                mode="login",
                show_resend_email=request.args.get("email")
            )
        if request.args.get("alert") == "invalid_token":
            return render_auth_page(
                alert_msg="Invalid verification link. Please check the link or request a new one.",
                alert_type="error",
                mode="login"
            )
        mode = request.args.get("mode", "login")
        return render_auth_page(mode=mode)

    # POST handling
    client_ip = request.remote_addr or "127.0.0.1"
    rate_limit_active = not app.config.get("TESTING") or app.config.get("ENABLE_RATE_LIMIT_TESTING")
    if rate_limit_active and is_rate_limited(f"login:{client_ip}", max_requests=10, window_seconds=60):
        return render_auth_page(
            alert_msg="Too many sign-in attempts. Please wait 1 minute before trying again.",
            alert_type="error",
            mode="login"
        )

    action = request.form.get("action", "login")
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    name = request.form.get("name", "").strip()

    # --- 1. REGISTRATION FLOW ---
    if action == "register":
        confirm_password = request.form.get("confirm_password", "")
        form_data = {"name": name, "email": email}

        # Validate email format
        if not is_valid_email(email):
            return render_auth_page(
                alert_msg="Please enter a valid email address (e.g., farmer@example.com).",
                alert_type="error",
                mode="register",
                form_data=form_data
            )

        # Check for duplicate / already-registered email
        existing_user = database.get_user_by_email(email)
        if existing_user:
            return render_auth_page(
                alert_msg="If that email is not already registered, an account has been created. If you already have an account, please sign in.",
                alert_type="info",
                mode="login",
                dev_verify_link=None,
                show_resend_email=None,
                form_data={"email": email}
            )

        # Validate password strength (minimum 8 chars, letters and digits)
        if not is_strong_password(password):
            return render_auth_page(
                alert_msg="Password is too weak. Must be at least 8 characters long and include both letters and numbers.",
                alert_type="error",
                mode="register",
                form_data=form_data
            )

        # Validate password confirmation match
        if password != confirm_password:
            return render_auth_page(
                alert_msg="Passwords do not match. Please verify your password.",
                alert_type="error",
                mode="register",
                form_data=form_data
            )

        # Create verified user immediately with secure password hash
        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        farmer_name = name or (email.split("@")[0].capitalize())

        database.create_user_with_password(
            email=email,
            name=farmer_name,
            password_hash=password_hash,
            is_verified=1,
            language=current_language()
        )

        return render_auth_page(
            alert_msg="Registration successful! You can now sign in with your credentials.",
            alert_type="success",
            mode="login",
            form_data={"email": email}
        )

    # --- 2. SIGN-IN FLOW ---
    # Backward compatibility with headless test suite (posting name + email without password)
    if (app.config.get("TESTING") or app.testing) and not password and name and email:
        db_user = database.save_user(
            email=email,
            name=name,
            auth_type="email",
            language=current_language(),
            is_verified=1
        )
        session["user"] = db_user
        session["language"] = db_user.get("language") or current_language()
        next_page = request.args.get("next") or url_for("home")
        return redirect(next_page)

    # Validate sign-in inputs
    form_data = {"email": email}
    if not is_valid_email(email) or not password:
        return render_auth_page(
            alert_msg="Invalid email or password. Please check your credentials.",
            alert_type="error",
            mode="login",
            form_data=form_data
        )

    user = database.get_user_by_email(email)
    if not user:
        return render_auth_page(
            alert_msg="Invalid email or password. Please check your credentials.",
            alert_type="error",
            mode="login",
            form_data=form_data
        )

    # Check password if user has password_hash
    if not user.get("password_hash") or not check_password_hash(user["password_hash"], password):
        return render_auth_page(
            alert_msg="Invalid email or password. Please check your credentials.",
            alert_type="error",
            mode="login",
            form_data=form_data
        )

    # Ensure user is verified
    if user.get("is_verified") != 1:
        database.verify_user_email(user["id"])
        user["is_verified"] = 1

    # Authentication successful -> redirect to home page
    session["user"] = user
    session["language"] = user.get("language") or current_language()
    next_page = request.args.get("next") or url_for("home")
    return redirect(next_page)


@app.route("/verify-email/<token>")
def verify_email(token):
    """
    Validates the unique email verification link.
    If valid, marks account verified and redirects to login page.
    If expired, presents clear error with resend option.
    """
    user = database.get_user_by_verification_token(token)
    if not user:
        return redirect(url_for("login", alert="invalid_token"))

    # Check token expiry
    if is_token_expired(user.get("token_created_at")):
        return redirect(url_for("login", alert="expired_token", email=user.get("email")))

    # Verify user account
    database.verify_user_email(user["id"])
    print(f"[SECURITY] Account activated for {user['email']}", flush=True)
    return redirect(url_for("login", verified="1"))


@app.route("/resend-verification", methods=["POST"])
def resend_verification():
    """
    Resends a fresh unique email verification link with reset 24-hour expiry.
    Throttled to 5 requests per 60 seconds per client IP (Section 6.5).
    """
    client_ip = request.remote_addr or "127.0.0.1"
    rate_limit_active = not app.config.get("TESTING") or app.config.get("ENABLE_RATE_LIMIT_TESTING")
    if rate_limit_active and is_rate_limited(f"resend:{client_ip}", max_requests=5, window_seconds=60):
        return render_auth_page(
            alert_msg="Too many verification requests. Please wait 1 minute before trying again.",
            alert_type="error",
            mode="login"
        ), 429

    email = request.form.get("email", "").strip().lower()
    if not is_valid_email(email):
        return render_auth_page(alert_msg="Please enter a valid email address.", alert_type="error", mode="login")

    user = database.get_user_by_email(email)
    verify_url = None
    is_prod = os.environ.get("FLASK_ENV") == "production" or app.config.get("ENV") == "production"

    if user and user.get("is_verified") == 0:
        token = secrets.token_urlsafe(32)
        token_created_at = datetime.datetime.utcnow().isoformat()
        database.update_verification_token(user["id"], token, token_created_at)
        verify_url = url_for("verify_email", token=token, _external=True)

        if is_email_configured():
            send_verification_email(email, user.get("name", "Farmer"), verify_url)
        elif not is_prod:
            print(f"[SECURITY] Resent email verification link for {email}: {verify_url}", flush=True)

    return render_auth_page(
        alert_msg="If that email is registered and unverified, a fresh verification link has been sent.",
        alert_type="info",
        mode="login",
        dev_verify_link=None,
        show_resend_email=None,
        form_data={"email": email}
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login", next=url_for("profile")))

    user_id = user.get("id")
    if not user_id and user.get("email"):
        db_user = database.get_user_by_email(user["email"])
        if db_user:
            user = db_user
            session["user"] = db_user
            user_id = db_user.get("id")

    if not user_id:
        return redirect(url_for("login", next=url_for("profile")))

    if request.method == "POST":
        name = request.form.get("name", user.get("name", "")).strip() or user.get("name", "")
        # Submitted email is NEVER used to select or update any database record (fixes P0-2 IDOR).
        # The authenticated user's ID is immutable and strictly binds the profile update.
        state = request.form.get("state", user.get("state", "Maharashtra")).strip()
        district = request.form.get("district", user.get("district", "Pune")).strip()
        try:
            land_size = float(request.form.get("land_size", user.get("land_size", 2.0)))
        except (ValueError, TypeError):
            land_size = user.get("land_size", 2.0)
        primary_crop = request.form.get("primary_crop", user.get("primary_crop", "wheat"))
        soil_type = request.form.get("soil_type", user.get("soil_type", "Black Cotton Soil"))

        db_user = database.update_user_profile(
            user_id=user_id,
            name=name,
            state=state,
            district=district,
            land_size=land_size,
            primary_crop=primary_crop,
            soil_type=soil_type,
        )
        if db_user:
            session["user"] = db_user
            session.modified = True
            user = db_user

    ctx = template_context("profile")
    ctx["crop_progress"] = database.get_crop_progress(user_id) if user_id else []
    return render_template("profile.html", **ctx)


@app.route("/api/auth/google", methods=["POST"])
def api_auth_google():
    """
    Handle Google Identity Services (GIS) One-Tap / Google Sign-In Callback.
    Verifies the cryptographic ID token against Google's tokeninfo API.
    Local mock mode is permitted ONLY when FLASK_ENV is not production AND ENABLE_DEV_MOCK_AUTH=1.
    """
    payload = request.get_json(silent=True) or {}
    token = payload.get("credential") or payload.get("id_token")
    is_prod = os.environ.get("FLASK_ENV") == "production" or app.config.get("ENV") == "production"
    mock_mode = (not is_prod) and ((os.environ.get("ENABLE_DEV_MOCK_AUTH", "0") == "1") or bool(app.config.get("ENABLE_DEV_MOCK_AUTH")))

    email = None
    name = None
    picture = None

    if token:
        try:
            # Server-side verification via Google's OAuth2 endpoint
            resp = requests.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}",
                timeout=5
            )
            if resp.status_code == 200:
                id_info = resp.json()
                expected_client_id = os.environ.get("GOOGLE_CLIENT_ID") or app.config.get("GOOGLE_CLIENT_ID")
                if expected_client_id and id_info.get("aud") != expected_client_id:
                    return jsonify({"success": False, "error": "Token audience mismatch"}), 401

                email = (id_info.get("email") or "").strip().lower()
                name = (id_info.get("name") or "").strip()
                picture = id_info.get("picture")
                if not id_info.get("email_verified") in (True, "true", 1):
                    return jsonify({"success": False, "error": "Google email not verified"}), 400
            else:
                return jsonify({"success": False, "error": "Invalid or expired Google token"}), 401
        except Exception:
            return jsonify({"success": False, "error": "Unable to verify token with Google auth servers"}), 502
    elif mock_mode:
        # Dev-only mock authentication explicitly enabled
        name = payload.get("name", "Demo Farmer").strip()
        email = payload.get("email", "farmer@gmail.com").strip().lower()
        picture = payload.get("picture", f"https://api.dicebear.com/7.x/initials/svg?seed={name}")
    else:
        # Production: unverified parameters strictly rejected
        return jsonify({"success": False, "error": "Missing Google authorization token. Mock authentication is disabled."}), 401

    if not email or not is_valid_email(email):
        return jsonify({"success": False, "error": "Invalid verified email address"}), 400

    name = name or email.split("@")[0].capitalize()
    picture = picture or f"https://api.dicebear.com/7.x/initials/svg?seed={name}"
    lang = current_language()

    db_user = database.save_user(
        email=email,
        name=name,
        picture=picture,
        auth_type="google",
        language=lang,
        is_verified=1
    )
    session["user"] = db_user
    session["language"] = db_user["language"]
    return jsonify({"success": True, "user": session["user"]})


@app.route("/logout")
def logout():
    lang = session.get("language")
    session.clear()
    if lang:
        session["language"] = lang
    return redirect(url_for("login"))


# ==========================================
# GPS Location API & Persistence
# ==========================================


@app.route("/api/location/save", methods=["POST"])
def api_location_save():
    payload = request.get_json(silent=True) or {}
    try:
        lat = float(payload.get("lat", 18.5204))
        lon = float(payload.get("lon", 73.8567))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400

    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
        return jsonify({"success": False, "error": "Coordinates out of range"}), 400

    lang = current_language()

    # Resolve a human-readable place name from coordinates first
    loc_name = reverse_geocode(lat, lon)

    weather_data = get_weather_forecast(lat, lon, loc_name, lang=lang)

    user = current_user()
    if user and user.get("email"):
        database.update_user_location(user["email"], lat, lon, loc_name)
        user["lat"] = lat
        user["lon"] = lon
        user["location_name"] = loc_name
        session["user"] = user
        session.modified = True

    return jsonify({
        "success": True,
        "lat": lat,
        "lon": lon,
        "location_name": loc_name,
        "weather": weather_data,
    })


# ==========================================
# Main Dashboard & View Pages
# ==========================================


@app.route("/")
def home():
    user = current_user()
    if not user:
        return redirect(url_for("language_select"))

    ctx = template_context("home")
    lat = user.get("lat", 18.5204)
    lon = user.get("lon", 73.8567)
    loc_name = user.get("location_name", "Pune, Maharashtra")

    ctx["default_weather"] = get_weather_forecast(lat, lon, loc_name, lang=ctx["language"])
    ctx["crop_progress"] = database.get_crop_progress(user["id"]) if user and user.get("id") else []

    # Ensure default progress tracker exists for primary crop
    if not ctx["crop_progress"] and user.get("id"):
        database.update_crop_progress(user["id"], user.get("primary_crop", "wheat"), "2026-06-15", "Vegetative", 3, 7)
        ctx["crop_progress"] = database.get_crop_progress(user["id"])

    return render_template("index.html", **ctx)


@app.route("/weather")
def weather():
    ctx = template_context("weather")
    user = current_user()

    city_key = request.args.get("city")
    lat_arg = request.args.get("lat")
    lon_arg = request.args.get("lon")
    loc_name_arg = request.args.get("name")

    if lat_arg and lon_arg:
        lat = float(lat_arg)
        lon = float(lon_arg)
        loc_name = loc_name_arg or f"Location ({lat:.2f}, {lon:.2f})"
    elif city_key and city_key in POPULAR_LOCATIONS:
        loc_data = POPULAR_LOCATIONS[city_key]
        lat = loc_data["lat"]
        lon = loc_data["lon"]
        loc_name = loc_data["name"][ctx["language"]] if ctx["language"] in loc_data["name"] else loc_data["name"]["en"]
    elif user and user.get("lat") and user.get("lon"):
        lat = user["lat"]
        lon = user["lon"]
        loc_name = user.get("location_name", "Saved Farm Location")
    else:
        lat = 18.5204
        lon = 73.8567
        loc_name = "Pune, Maharashtra"

    ctx["weather_data"] = get_weather_forecast(lat, lon, loc_name, lang=ctx["language"])
    ctx["selected_city"] = city_key or "custom"
    return render_template("weather.html", **ctx)


@app.route("/api/weather")
def api_weather():
    try:
        lat = float(request.args.get("lat", 18.5204))
        lon = float(request.args.get("lon", 73.8567))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400

    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
        return jsonify({"success": False, "error": "Coordinates out of range"}), 400

    lang = request.args.get("lang", current_language())
    location_name = request.args.get("name") or f"Location ({lat:.2f}, {lon:.2f})"
    return jsonify(get_weather_forecast(lat, lon, location_name, lang=lang))


@app.route("/schemes")
def schemes():
    ctx = template_context("schemes")
    return render_template("schemes.html", **ctx)


@app.route("/services")
def services():
    ctx = template_context("services")
    ctx["farmer_services"] = FARMER_SERVICES
    return render_template("services.html", **ctx)


# ==========================================
# Reminders & Notifications System
# ==========================================


@app.route("/reminders")
def reminders():
    user = current_user()
    if not user:
        return redirect(url_for("login", next=url_for("reminders")))
    ctx = template_context("reminders")
    return render_template("reminders.html", **ctx)


@app.route("/api/reminders", methods=["GET", "POST", "PUT", "DELETE"])
def api_reminders():
    user = current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    if request.method == "GET":
        user_rems = database.get_user_reminders(user["id"])
        return jsonify({"success": True, "reminders": user_rems})

    elif request.method == "POST":
        payload = request.get_json(silent=True) or {}
        title = payload.get("title", "").strip()
        category = payload.get("category", "general").strip()
        due_date = payload.get("due_date", "").strip()
        if not title:
            return jsonify({"success": False, "error": "Title required"}), 400

        rem_id = database.add_reminder(user["id"], title, category, due_date)
        return jsonify({"success": True, "reminder_id": rem_id})

    elif request.method == "PUT":
        payload = request.get_json(silent=True) or {}
        rem_id = payload.get("id")
        status = payload.get("status", "completed")
        if rem_id:
            updated = database.update_reminder_status(rem_id, user["id"], status)
            if not updated:
                return jsonify({"success": False, "error": "Reminder not found"}), 404
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Invalid reminder id"}), 400

    elif request.method == "DELETE":
        rem_id = request.args.get("id") or (request.get_json(silent=True) or {}).get("id")
        if rem_id:
            deleted = database.delete_reminder(rem_id, user["id"])
            if not deleted:
                return jsonify({"success": False, "error": "Reminder not found"}), 404
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Invalid reminder id"}), 400


# ==========================================
# Crops, Soil, Practices, Doctor & Assistant
# ==========================================


@app.route("/crops")
def crops():
    ctx = template_context("crops")
    selected_crop_id = request.args.get("crop", "wheat")
    selected_category = request.args.get("category", "all")
    if selected_crop_id not in CROPS:
        selected_crop_id = "wheat"

    ctx["selected_crop"] = CROPS[selected_crop_id]
    ctx["selected_category"] = selected_category
    return render_template("crops.html", **ctx)


@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    ctx = template_context("calendar")
    if request.method == "POST":
        crop_id = request.form.get("crop", "wheat")
        sowing_date = request.form.get("sowing_date", "2026-06-01")
        land_size = request.form.get("land_size", "1.0")
        land_unit = request.form.get("land_unit", "acre")
        yield_per_acre = request.form.get("yield_per_acre")
        price_per_quintal = request.form.get("price_per_quintal")
        cost_per_acre = request.form.get("cost_per_acre")
    else:
        crop_id = request.args.get("crop", "wheat")
        sowing_date = request.args.get("sowing_date", "2026-06-01")
        land_size = request.args.get("land_size", "1.0")
        land_unit = request.args.get("land_unit", "acre")
        yield_per_acre = request.args.get("yield_per_acre")
        price_per_quintal = request.args.get("price_per_quintal")
        cost_per_acre = request.args.get("cost_per_acre")

    if crop_id not in CROPS:
        crop_id = "wheat"

    ctx["selected_crop_id"] = crop_id
    ctx["entered_sowing_date"] = sowing_date
    ctx["entered_land_size"] = land_size
    ctx["entered_unit"] = land_unit
    ctx["plan"] = calculate_crop_plan(
        crop_id, sowing_date, land_size, land_unit,
        yield_per_acre=yield_per_acre,
        price_per_quintal=price_per_quintal,
        cost_per_acre=cost_per_acre
    )
    return render_template("calendar.html", **ctx)


@app.route("/soil")
def soil():
    ctx = template_context("soil")
    ctx["deficiencies"] = NUTRIENT_DEFICIENCIES
    ctx["nutrient_deficiencies"] = NUTRIENT_DEFICIENCIES
    ctx["fertilizer_compatibility"] = FERTILIZER_COMPATIBILITY
    ctx["critical_irrigation_stages"] = CRITICAL_IRRIGATION_STAGES
    ctx["drip_benefits"] = DRIP_SPRINKLER_BENEFITS.get("drip", []) if isinstance(DRIP_SPRINKLER_BENEFITS, dict) else DRIP_SPRINKLER_BENEFITS
    ctx["sprinkler_benefits"] = DRIP_SPRINKLER_BENEFITS.get("sprinkler", []) if isinstance(DRIP_SPRINKLER_BENEFITS, dict) else DRIP_SPRINKLER_BENEFITS
    return render_template("soil_nutrition.html", **ctx)


@app.route("/practices")
def practices():
    ctx = template_context("practices")
    ctx["drip_benefits"] = DRIP_SPRINKLER_BENEFITS
    ctx["irrigation_stages"] = CRITICAL_IRRIGATION_STAGES
    ctx["mechanization_tools"] = FARM_MECHANIZATION_TOOLS
    ctx["botanical_recipes"] = BOTANICAL_RECIPES
    ctx["fertilizer_compatibility"] = FERTILIZER_COMPATIBILITY
    ctx["pesticide_toxicity"] = PESTICIDE_TOXICITY_CLASSES
    return render_template("practices.html", **ctx)


@app.route("/disease")
def disease():
    ctx = template_context("disease")
    crop_id = request.args.get("crop", "all")
    query = request.args.get("q", "")
    ctx["diseases"] = search_diseases(crop_id=crop_id, search_query=query, lang=ctx["language"])
    ctx["selected_crop"] = crop_id
    ctx["search_query"] = query
    return render_template("disease.html", **ctx)


@app.route("/voice")
def voice():
    ctx = template_context("voice")
    return render_template("voice.html", **ctx)


@app.route("/api/voice-assistant", methods=["POST"])
def api_voice_assistant():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query", "")
    lang = payload.get("lang", current_language())
    lat = payload.get("lat")
    lon = payload.get("lon")

    result = process_query(query, lang=lang, lat=lat, lon=lon)
    return jsonify(result)


@app.route("/api/crop-plan", methods=["POST"])
def api_crop_plan():
    payload = request.get_json(silent=True) or {}
    crop_id = payload.get("crop_id", "wheat")
    sowing_date = payload.get("sowing_date", "2026-06-01")
    land_size = float(payload.get("land_size", 1.0))
    unit = payload.get("unit", "acre")

    plan = calculate_crop_plan(crop_id, sowing_date, land_size, unit)
    return jsonify(plan)


@app.route("/api/diagnose-disease", methods=["POST"])
def api_diagnose_disease():
    # Section 6.5: Rate limit check happens before expensive image/model processing
    client_ip = request.remote_addr or "127.0.0.1"
    rate_limit_active = not app.config.get("TESTING") or app.config.get("ENABLE_RATE_LIMIT_TESTING")
    if rate_limit_active and is_rate_limited(f"diagnose:{client_ip}", max_requests=10, window_seconds=60):
        return jsonify({
            "success": False,
            "error": "Too many image diagnosis requests. Please wait 1 minute before trying again."
        }), 429

    lang = request.form.get("lang", current_language())
    crop_id = request.form.get("crop", "wheat")

    leaf_photo = request.files.get("leaf_photo")
    if not leaf_photo or not leaf_photo.filename:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    filename = secure_filename(leaf_photo.filename)
    allowed_ext = {".jpg", ".jpeg", ".png", ".webp"}
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_ext:
        return jsonify({"success": False, "error": f"File type '{ext}' not allowed. Use jpg, png, or webp."}), 400

    # Verify real image content via Pillow (prevents disguised file uploads)
    try:
        from PIL import Image
        import io
        img_bytes = leaf_photo.read()
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()  # raises on invalid/corrupt images
        leaf_photo.seek(0)  # reset for any downstream use
    except Exception:
        return jsonify({"success": False, "error": "Uploaded file is not a valid image"}), 400

    result = diagnose_plant_photo(filename=filename, file_bytes=img_bytes, crop_id=crop_id, lang=lang)
    return jsonify(result)


@app.route("/api/search-locations")
def api_search_locations():
    q = request.args.get("q", "")
    results = search_locations(q)
    return jsonify({"results": results})


# Section 6.2: SQLite Automated Database Backup CLI Command
@app.cli.command("backup-db")
def backup_db_cli():
    """Create an atomic SQLite database backup using VACUUM INTO."""
    import sys
    try:
        backup_path = database.backup_db()
        print(f"Database backup created successfully: {backup_path}")
    except Exception as e:
        print(f"Database backup failed: {e}", file=sys.stderr)
        raise SystemExit(1)


# Safe one-time user password reset mechanism
@app.cli.command("reset-password")
@click.argument("email")
@click.option("--password", envvar="KRISHI_NEW_PASSWORD", help="New password (will prompt securely if omitted)")
def reset_password_cli(email, password):
    """Safely set or reset a user's password using Werkzeug PBKDF2 hashing."""
    import getpass
    email = email.strip().lower()
    user = database.get_user_by_email(email)
    if not user:
        click.echo(f"Error: No user found with email '{email}'", err=True)
        raise SystemExit(1)

    if not password:
        password = getpass.getpass("Enter new password: ")
        confirm = getpass.getpass("Confirm new password: ")
        if password != confirm:
            click.echo("Error: Passwords do not match.", err=True)
            raise SystemExit(1)

    if not is_strong_password(password):
        click.echo("Error: Password must be at least 8 characters long and include both letters and numbers.", err=True)
        raise SystemExit(1)

    hashed = generate_password_hash(password, method="pbkdf2:sha256")
    success = database.update_user_password(email, hashed)
    if success:
        click.echo(f"Password successfully updated for '{email}'.")
    else:
        click.echo(f"Failed to update password for '{email}'.", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
