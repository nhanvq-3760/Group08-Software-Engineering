-- Local demo/test database only; DO NOT run on Authentication/phonebook.db.
-- User columns intentionally match Authentication/database/connection.py exactly.
-- Demo uses non-login placeholder hashes; real accounts must come from Authentication.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "User" (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Contact" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES "User"("UserID") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_contacts_user ON "Contact"(user_id);

CREATE TABLE IF NOT EXISTS "Phone_Number" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    phone_number TEXT NOT NULL,
    label TEXT NOT NULL DEFAULT 'mobile',
    FOREIGN KEY (contact_id) REFERENCES "Contact"(id) ON DELETE CASCADE,
    UNIQUE (contact_id, phone_number)
);
