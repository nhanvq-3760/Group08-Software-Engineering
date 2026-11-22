-- SQLite integration schema for ContactManagement + existing Authentication.
-- IMPORTANT: Authentication/database/connection.py owns "User".
-- Initialize Authentication's User table BEFORE applying this file.
-- The existing User PK is UserID (not id). Do NOT rename User columns.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "Contact" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL CHECK (length(trim(full_name)) > 0),
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
