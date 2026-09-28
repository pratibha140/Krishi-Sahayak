# local_auth_check.py
# Interactive Read-Only Authentication Diagnostic Utility for Krishi Sahayak
# Prompts for password securely without echo, checks Werkzeug hash, and tests Flask test client.

import getpass
import sys
from werkzeug.security import check_password_hash
import database
from app import app

print("=" * 60)
print("KRISHI SAHAYAK - LOCAL READ-ONLY AUTHENTICATION DIAGNOSTIC")
print("=" * 60)

# 1. Database Path & Account Info
db_path = database.get_db_path()
print(f"Database path: {db_path}")

target_emails = [
    "pratibha.pawar2006@gmail.com",
    "pawarpratibha2006@gmail.com",
    "pratibhapawar@gmail.com"
]

users = {}
for e in target_emails:
    u = database.get_user_by_email(e)
    users[e] = u
    found = "YES" if u else "NO"
    has_hash = "YES" if (u and u.get("password_hash")) else "NO"
    verif = "YES" if (u and u.get("is_verified") == 1) else "NO"
    print(f"\nAccount [{e}]:")
    print(f"  Account found: {found}")
    print(f"  Hash present:  {has_hash}")
    print(f"  Verified:      {verif}")

print("\n" + "-" * 60)
# 2. Interactive Password Prompt (No Echo)
try:
    password = getpass.getpass("Enter password to test against database (input hidden): ")
except (KeyboardInterrupt, EOFError):
    print("\nAborted.")
    sys.exit(0)

print("-" * 60)

# 3. Hash Match Verification
primary_email = "pratibha.pawar2006@gmail.com"
primary_user = users.get(primary_email)

primary_match = False
if primary_user and primary_user.get("password_hash"):
    primary_match = check_password_hash(primary_user["password_hash"], password)
    result_str = "YES" if primary_match else "NO"
    print(f"PASSWORD HASH MATCH ({primary_email}) = {result_str}")
else:
    print(f"PASSWORD HASH MATCH ({primary_email}) = NO (no hash stored)")

for e in target_emails[1:]:
    u = users.get(e)
    if u and u.get("password_hash"):
        m = check_password_hash(u["password_hash"], password)
        print(f"PASSWORD HASH MATCH ({e}) = {'YES' if m else 'NO'}")
    else:
        print(f"PASSWORD HASH MATCH ({e}) = NO (no hash stored)")

print("-" * 60)

# 4. Actual Flask Login Route Simulation via Test Client
print("FLASK TEST-CLIENT LOGIN EXECUTION:")
client = app.test_client()

# Fetch CSRF token
client.get("/login")
with client.session_transaction() as sess:
    csrf_token = sess.get("_csrf_token")

res = client.post("/login", data={
    "action": "login",
    "email": primary_email,
    "password": password,
    "csrf_token": csrf_token
}, follow_redirects=False)

status = res.status_code
location = res.headers.get("Location", "None")
html = res.get_data(as_text=True)
has_invalid_msg = "Invalid email or password. Please check your credentials." in html

with client.session_transaction() as sess:
    logged_in_user = sess.get("user")
    has_auth_user = bool(logged_in_user and logged_in_user.get("email") == primary_email)

print(f"  HTTP status: {status}")
print(f"  Redirect location: {location}")
print(f"  Contains 'Invalid email or password': {'YES' if has_invalid_msg else 'NO'}")
print(f"  Session contains authenticated user: {'YES' if has_auth_user else 'NO'}")

# 5. Determine Exact Failing Branch
print("-" * 60)
if not primary_user:
    branch = "A (user not found in database)"
elif not primary_user.get("password_hash"):
    branch = "C (password_hash missing/NULL in database)"
elif not primary_match:
    branch = "D (check_password_hash returns False — password entered does NOT match stored hash)"
elif primary_user.get("is_verified") != 1:
    branch = "E (account is_verified != 1)"
elif status == 302 and has_auth_user:
    branch = "NONE (Login succeeds! Both hash check and session creation passed)"
else:
    branch = "F (other condition)"

print(f"EXACT FAILING BRANCH: {branch}")
print("=" * 60)
