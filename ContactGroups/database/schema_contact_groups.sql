PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "Contact_Group" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_name TEXT NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES "User"("UserID") ON DELETE CASCADE,
    UNIQUE (user_id, group_name)
);

CREATE TABLE IF NOT EXISTS "Contact_Group_Member" (
    group_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    PRIMARY KEY (group_id, contact_id),
    FOREIGN KEY (group_id)
        REFERENCES "Contact_Group"(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id)
        REFERENCES "Contact"(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_contact_group_user
ON "Contact_Group"(user_id);

CREATE INDEX IF NOT EXISTS idx_contact_group_member_contact
ON "Contact_Group_Member"(contact_id);
