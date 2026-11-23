"""SQLite database layer for Phone Book Management System."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("phonebook.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Contact (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT,
    address TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Phone_Number (
    phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    phone_number TEXT NOT NULL,
    phone_type TEXT DEFAULT 'mobile',
    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE,
    UNIQUE (contact_id, phone_number)
);

CREATE TABLE IF NOT EXISTS Contact_Group (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    UNIQUE (user_id, group_name)
);

CREATE TABLE IF NOT EXISTS Contact_Group_Member (
    group_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    PRIMARY KEY (group_id, contact_id),
    FOREIGN KEY (group_id) REFERENCES Contact_Group(group_id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_contact_user ON Contact(user_id);
CREATE INDEX IF NOT EXISTS idx_group_user ON Contact_Group(user_id);
CREATE INDEX IF NOT EXISTS idx_phone_contact ON Phone_Number(contact_id);
"""

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)

def check_integrity(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    return {"foreign_key_errors": [tuple(row) for row in fk_errors],
            "integrity_check": integrity}
