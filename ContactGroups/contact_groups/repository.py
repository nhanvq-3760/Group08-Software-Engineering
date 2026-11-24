"""SQLite repository for group records and memberships.

Expected schema: Contact_Group(id, user_id, group_name),
Contact_Group_Member(group_id, contact_id). Member 4 owns final migrations.
"""
import sqlite3
from .models import ContactGroup, GroupNotFound, ContactNotFound, GroupValidationError

class SQLiteGroupRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.db = connection
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")

    def create_group(self, user_id: int, name: str) -> ContactGroup:
        try:
            with self.db:
                cur = self.db.execute('INSERT INTO "Contact_Group" (user_id, group_name) VALUES (?, ?)', (user_id, name))
            return ContactGroup(cur.lastrowid, user_id, name)
        except sqlite3.IntegrityError as e:
            raise GroupValidationError("Group name already exists or user_id is invalid") from e

    def list_groups(self, user_id: int) -> list[ContactGroup]:
        rows = self.db.execute('SELECT id, user_id, group_name FROM "Contact_Group" WHERE user_id=? ORDER BY group_name COLLATE NOCASE, id', (user_id,)).fetchall()
        return [self.get_group(user_id, row['id']) for row in rows]

    def get_group(self, user_id: int, group_id: int) -> ContactGroup | None:
        row = self.db.execute('SELECT id, user_id, group_name FROM "Contact_Group" WHERE id=? AND user_id=?', (group_id, user_id)).fetchone()
        if not row: return None
        members = self.db.execute('''SELECT c.id, c.full_name, c.email, c.address
            FROM "Contact_Group_Member" gm JOIN "Contact" c ON c.id=gm.contact_id
            WHERE gm.group_id=? AND c.user_id=? ORDER BY c.full_name COLLATE NOCASE''', (group_id, user_id)).fetchall()
        contacts = tuple(dict(m) for m in members)
        return ContactGroup(row['id'], row['user_id'], row['group_name'], contacts)

    def rename_group(self, user_id: int, group_id: int, name: str) -> ContactGroup:
        try:
            with self.db:
                cur = self.db.execute('UPDATE "Contact_Group" SET group_name=? WHERE id=? AND user_id=?', (name, group_id, user_id))
                if cur.rowcount != 1: raise GroupNotFound("Group not found")
        except sqlite3.IntegrityError as e:
            raise GroupValidationError("Group name already exists") from e
        return self.get_group(user_id, group_id)

    def delete_group(self, user_id: int, group_id: int) -> bool:
        with self.db:
            cur = self.db.execute('DELETE FROM "Contact_Group" WHERE id=? AND user_id=?', (group_id, user_id))
        return cur.rowcount == 1

    def add_contact(self, user_id: int, group_id: int, contact_id: int) -> None:
        group = self.db.execute('SELECT id FROM "Contact_Group" WHERE id=? AND user_id=?', (group_id, user_id)).fetchone()
        contact = self.db.execute('SELECT id FROM "Contact" WHERE id=? AND user_id=?', (contact_id, user_id)).fetchone()
        if not group: raise GroupNotFound("Group not found")
        if not contact: raise ContactNotFound("Contact not found")
        try:
            with self.db:
                self.db.execute('INSERT INTO "Contact_Group_Member" (group_id, contact_id) VALUES (?, ?)', (group_id, contact_id))
        except sqlite3.IntegrityError as e:
            raise GroupValidationError("Contact is already in this group") from e

    def remove_contact(self, user_id: int, group_id: int, contact_id: int) -> bool:
        group = self.db.execute('SELECT id FROM "Contact_Group" WHERE id=? AND user_id=?', (group_id, user_id)).fetchone()
        if not group: raise GroupNotFound("Group not found")
        cur = self.db.execute('DELETE FROM "Contact_Group_Member" WHERE group_id=? AND contact_id=?', (group_id, contact_id))
        return cur.rowcount == 1
