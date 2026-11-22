-- PROPOSAL ONLY: Member 3 and Member 4 must agree BEFORE applying.
-- Assumes the Authentication User and Contact tables already exist.
-- This is NOT automatically executed by initialize_contact_tables().
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "Contact_Group" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "User"("UserID") ON DELETE CASCADE,
    UNIQUE (user_id, group_name)
);

CREATE TABLE IF NOT EXISTS "Contact_Group_Member" (
    group_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    PRIMARY KEY (group_id, contact_id),
    FOREIGN KEY (group_id) REFERENCES "Contact_Group"(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES "Contact"(id) ON DELETE CASCADE
);

-- Prevent cross-user group membership at database level, even if UI checks fail.
CREATE TRIGGER IF NOT EXISTS trg_cgm_same_user_insert
BEFORE INSERT ON "Contact_Group_Member"
FOR EACH ROW WHEN (
    (SELECT user_id FROM "Contact_Group" WHERE id = NEW.group_id) IS NOT
    (SELECT user_id FROM "Contact" WHERE id = NEW.contact_id)
)
BEGIN
    SELECT RAISE(ABORT, 'A group may contain only contacts owned by the same user');
END;

CREATE TRIGGER IF NOT EXISTS trg_cgm_same_user_update
BEFORE UPDATE OF group_id, contact_id ON "Contact_Group_Member"
FOR EACH ROW WHEN (
    (SELECT user_id FROM "Contact_Group" WHERE id = NEW.group_id) IS NOT
    (SELECT user_id FROM "Contact" WHERE id = NEW.contact_id)
)
BEGIN
    SELECT RAISE(ABORT, 'A group may contain only contacts owned by the same user');
END;
