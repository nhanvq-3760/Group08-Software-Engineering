
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "phonebook.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS User (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserName TEXT NOT NULL UNIQUE,
                PasswordHash TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(User)").fetchall()
        }

        if "role" not in columns:
            conn.execute("""
                ALTER TABLE User
                ADD COLUMN role TEXT NOT NULL DEFAULT 'user'
                CHECK (role IN ('user', 'admin'))
            """)

        if "is_active" not in columns:
            conn.execute("""
                ALTER TABLE User
                ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1
                CHECK (is_active IN (0, 1))
            """)
