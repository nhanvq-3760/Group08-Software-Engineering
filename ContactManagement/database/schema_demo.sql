-- DEMO/TEST-ONLY SQLite schema. Member 4 owns the production schema.
-- Three of the five project tables are needed to test Member 2 independently.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "User" (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "Contact" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE
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
