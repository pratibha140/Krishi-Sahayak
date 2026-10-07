# database.py
# SQLite Database Persistence Module for Krishi Sahayak
# Manages user accounts, language preferences, saved GPS location, farm profile, crop progress & reminders.

import datetime
import os
import re
import sqlite3
import time

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
DB_PATH = DEFAULT_DB_PATH  # Maintained for backward compatibility
DEFAULT_BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
BACKUP_FILENAME_PREFIX = "krishi_sahayak_backup_"
BACKUP_FILENAME_PATTERN = re.compile(r"^krishi_sahayak_backup_\d{8}_\d{6}\.db$")


def get_db_path():
    """
    Resolves the active SQLite database path.
    1. Reads DATABASE_PATH from the environment.
    2. If unset, empty, or whitespace, falls back to <project root>/database.db.
    3. Ensures the parent directory exists before returning.
    """
    env_path = os.environ.get("DATABASE_PATH")
    if env_path and env_path.strip():
        resolved = os.path.abspath(env_path.strip())
    else:
        resolved = os.path.abspath(DEFAULT_DB_PATH)

    parent_dir = os.path.dirname(resolved)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    return resolved


def get_db_connection(db_path=None):
    if db_path is None:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_db_connection(db_path=db_path)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT,
            is_verified INTEGER DEFAULT 0,
            verification_token TEXT,
            token_created_at TIMESTAMP,
            picture TEXT,
            auth_type TEXT DEFAULT 'email',
            language TEXT DEFAULT 'en',
            phone TEXT,
            state TEXT DEFAULT 'Maharashtra',
            district TEXT DEFAULT 'Pune',
            lat REAL DEFAULT 18.5204,
            lon REAL DEFAULT 73.8567,
            location_name TEXT DEFAULT 'Pune, Maharashtra',
            land_size REAL DEFAULT 2.0,
            primary_crop TEXT DEFAULT 'wheat',
            soil_type TEXT DEFAULT 'Black Cotton Soil',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migration check for existing users table
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    if "password_hash" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    if "is_verified" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
    if "verification_token" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN verification_token TEXT")
    if "token_created_at" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN token_created_at TIMESTAMP")

    # Reminders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    # Crop Progress Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crop_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            crop_id TEXT NOT NULL,
            sowing_date TEXT NOT NULL,
            current_stage TEXT DEFAULT 'Vegetative',
            tasks_completed INTEGER DEFAULT 2,
            total_tasks INTEGER DEFAULT 6,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    # Performance Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_verif_token ON users(verification_token);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reminders_user_id ON reminders(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_crop_progress_user ON crop_progress(user_id);")

    conn.commit()
    conn.close()


def get_user_by_email(email):
    if not email:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_user_with_password(email, name, password_hash, verification_token=None, token_created_at=None, picture=None, auth_type="email", language="en", is_verified=1):
    email = email.strip().lower()
    name = name.strip()
    picture = picture or f"https://api.dicebear.com/7.x/initials/svg?seed={name}"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, name, password_hash, is_verified, verification_token, token_created_at, picture, auth_type, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (email, name, password_hash, is_verified, verification_token, token_created_at, picture, auth_type, language))
    conn.commit()
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_verification_token(token):
    if not token:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE verification_token = ?", (token.strip(),)).fetchone()
    conn.close()
    return dict(user) if user else None


def verify_user_email(user_id):
    conn = get_db_connection()
    conn.execute("UPDATE users SET is_verified = 1, verification_token = NULL WHERE id = ?", (user_id,))
    conn.commit()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_verification_token(user_id, token, token_created_at):
    conn = get_db_connection()
    conn.execute("UPDATE users SET verification_token = ?, token_created_at = ? WHERE id = ?", (token, token_created_at, user_id))
    conn.commit()
    conn.close()


def save_user(email, name, picture=None, auth_type="email", language="en", state="Maharashtra", district="Pune", lat=18.5204, lon=73.8567, location_name="Pune, Maharashtra", land_size=2.0, primary_crop="wheat", soil_type="Black Cotton Soil", is_verified=None, password_hash=None):
    email = email.strip().lower()
    picture = picture or f"https://api.dicebear.com/7.x/initials/svg?seed={name}"
    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        cursor.execute("""
            UPDATE users SET
                name = ?, picture = ?, auth_type = ?, language = COALESCE(?, language),
                state = COALESCE(?, state), district = COALESCE(?, district),
                lat = COALESCE(?, lat), lon = COALESCE(?, lon), location_name = COALESCE(?, location_name),
                land_size = COALESCE(?, land_size), primary_crop = COALESCE(?, primary_crop),
                soil_type = COALESCE(?, soil_type),
                is_verified = COALESCE(?, is_verified),
                password_hash = COALESCE(?, password_hash)
            WHERE email = ?
        """, (name, picture, auth_type, language, state, district, lat, lon, location_name, land_size, primary_crop, soil_type, is_verified, password_hash, email))
    else:
        # Default is_verified = 1 for Google or legacy save_user calls if not explicitly set
        verified_val = 1 if is_verified is None else is_verified
        cursor.execute("""
            INSERT INTO users (email, name, picture, auth_type, language, state, district, lat, lon, location_name, land_size, primary_crop, soil_type, is_verified, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (email, name, picture, auth_type, language, state, district, lat, lon, location_name, land_size, primary_crop, soil_type, verified_val, password_hash))

    conn.commit()
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    if not user_id:
        return None
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user_profile(user_id, name, state=None, district=None, land_size=None, primary_crop=None, soil_type=None):
    """
    Safely updates a user's profile information by their immutable user ID.
    Email cannot be modified via this function to prevent IDOR / Account Takeover.
    """
    if not user_id:
        return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET
            name = ?,
            state = COALESCE(?, state),
            district = COALESCE(?, district),
            land_size = COALESCE(?, land_size),
            primary_crop = COALESCE(?, primary_crop),
            soil_type = COALESCE(?, soil_type)
        WHERE id = ?
    """, (name, state, district, land_size, primary_crop, soil_type, user_id))
    conn.commit()
    user = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user_language(email, language):
    if not email:
        return
    conn = get_db_connection()
    conn.execute("UPDATE users SET language = ? WHERE email = ?", (language, email.strip().lower()))
    conn.commit()
    conn.close()


def update_user_location(email, lat, lon, location_name):
    if not email:
        return
    conn = get_db_connection()
    conn.execute("UPDATE users SET lat = ?, lon = ?, location_name = ? WHERE email = ?", (lat, lon, location_name, email.strip().lower()))
    conn.commit()
    conn.close()


def update_user_password(email, password_hash):
    """Safely updates a user's password hash and marks account as verified."""
    if not email or not password_hash:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET password_hash = ?, is_verified = 1 WHERE email = ?
    """, (password_hash, email.strip().lower()))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def get_user_reminders(user_id):
    conn = get_db_connection()
    reminders = conn.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY due_date ASC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in reminders]


def add_reminder(user_id, title, category="general", due_date=None):
    if not due_date:
        due_date = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reminders (user_id, title, category, due_date, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (user_id, title, category, due_date))
    conn.commit()
    rem_id = cursor.lastrowid
    conn.close()
    return rem_id


def update_reminder_status(reminder_id, user_id=None, status="completed"):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("UPDATE reminders SET status = ? WHERE id = ? AND user_id = ?", (status, reminder_id, user_id))
    else:
        cursor.execute("UPDATE reminders SET status = ? WHERE id = ?", (status, reminder_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_reminder(reminder_id, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("DELETE FROM reminders WHERE id = ? AND user_id = ?", (reminder_id, user_id))
    else:
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def get_crop_progress(user_id):
    conn = get_db_connection()
    progress = conn.execute("SELECT * FROM crop_progress WHERE user_id = ? ORDER BY updated_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(p) for p in progress]


def update_crop_progress(user_id, crop_id, sowing_date, current_stage="Vegetative", tasks_completed=2, total_tasks=6):
    conn = get_db_connection()
    cursor = conn.cursor()
    existing = cursor.execute("SELECT id FROM crop_progress WHERE user_id = ? AND crop_id = ?", (user_id, crop_id)).fetchone()
    if existing:
        cursor.execute("""
            UPDATE crop_progress SET sowing_date = ?, current_stage = ?, tasks_completed = ?, total_tasks = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (sowing_date, current_stage, tasks_completed, total_tasks, existing["id"]))
    else:
        cursor.execute("""
            INSERT INTO crop_progress (user_id, crop_id, sowing_date, current_stage, tasks_completed, total_tasks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, crop_id, sowing_date, current_stage, tasks_completed, total_tasks))
    conn.commit()
    conn.close()


def prune_backups(backup_dir=DEFAULT_BACKUP_DIR, keep_count=7, current_db_path=None):
    """
    Prunes older backups in backup_dir matching BACKUP_FILENAME_PATTERN,
    retaining only the newest `keep_count` files.
    
    Safeguards:
    - Never deletes the active database (current_db_path).
    - Never deletes files outside backup_dir.
    - Only deletes files matching BACKUP_FILENAME_PATTERN.
    """
    if keep_count is None or keep_count < 1:
        return []

    if current_db_path is None:
        current_db_path = get_db_path()

    backup_dir = os.path.abspath(backup_dir)
    if not os.path.isdir(backup_dir):
        return []

    active_db_abs = os.path.abspath(current_db_path)
    matching_backups = []

    for entry in os.listdir(backup_dir):
        entry_path = os.path.join(backup_dir, entry)
        if os.path.isfile(entry_path) and BACKUP_FILENAME_PATTERN.match(entry):
            if os.path.abspath(entry_path) != active_db_abs:
                matching_backups.append(entry_path)

    # Sort matching files chronologically by filename (timestamp format YYYYMMDD_HHMMSS)
    matching_backups.sort(key=lambda p: os.path.basename(p))

    deleted_files = []
    if len(matching_backups) > keep_count:
        excess_count = len(matching_backups) - keep_count
        to_delete = matching_backups[:excess_count]
        for file_path in to_delete:
            abs_p = os.path.abspath(file_path)
            # Strict safety checks before deletion
            if (
                abs_p != active_db_abs
                and os.path.dirname(abs_p) == backup_dir
                and BACKUP_FILENAME_PATTERN.match(os.path.basename(abs_p))
            ):
                try:
                    os.remove(abs_p)
                    deleted_files.append(abs_p)
                except OSError:
                    pass

    return deleted_files


def backup_db(backup_dir=None, keep_count=7, db_path=None):
    """
    Creates an atomic, point-in-time SQLite backup using SQLite's native VACUUM INTO statement.
    Preserves active WAL mode transactions, defragments the destination database,
    and prunes older backups beyond keep_count.

    :param backup_dir: Directory where the backup will be stored (defaults to <project root>/backups).
    :param keep_count: Number of most recent backups to retain (defaults to 7).
    :param db_path: Source database path (defaults to resolved get_db_path()).
    :return: Absolute path string of the created backup database file.
    """
    if keep_count is not None and (not isinstance(keep_count, int) or keep_count < 1):
        raise ValueError("keep_count must be a positive integer >= 1")

    if db_path is None:
        db_path = get_db_path()

    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Source database file not found: {db_path}")

    if backup_dir is None:
        backup_dir = DEFAULT_BACKUP_DIR
    backup_dir = os.path.abspath(backup_dir)

    # 1. Ensure target directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # 2. Generate unique timestamped filename
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    target_filename = f"{BACKUP_FILENAME_PREFIX}{timestamp_str}.db"
    target_path = os.path.join(backup_dir, target_filename)

    # Prevent collision if executed within the same second
    if os.path.exists(target_path):
        time.sleep(1.05)
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        target_filename = f"{BACKUP_FILENAME_PREFIX}{timestamp_str}.db"
        target_path = os.path.join(backup_dir, target_filename)
        if os.path.exists(target_path):
            raise RuntimeError(f"Backup target file already exists: {target_path}")

    # 3. Execute VACUUM INTO via short-lived independent SQLite connection
    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        # Parameterized query - never string interpolation
        conn.execute("VACUUM INTO ?", (target_path,))
    except Exception as e:
        if os.path.exists(target_path):
            try:
                os.remove(target_path)
            except OSError:
                pass
        raise RuntimeError(f"Database backup failed via VACUUM INTO: {e}") from e
    finally:
        if conn:
            conn.close()

    # 4. Retention management: prune older backups matching pattern
    if keep_count is not None:
        try:
            prune_backups(backup_dir=backup_dir, keep_count=keep_count, current_db_path=db_path)
        except Exception:
            pass

    return os.path.abspath(target_path)


if __name__ == "__main__":
    init_db()

