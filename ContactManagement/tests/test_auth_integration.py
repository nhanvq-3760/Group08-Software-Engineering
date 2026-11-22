"""Integration-contract regression tests for SQLite Authentication.UserID.

Run from the ContactManagement folder:
    python -m unittest discover -s tests -v
"""
import sqlite3
import unittest
from pathlib import Path

from contact_management.auth_integration import (
    SchemaCompatibilityError,
    initialize_contact_tables,
)

ROOT = Path(__file__).resolve().parents[1]

# Exactly the production Authentication User DDL published in
# Authentication/database/connection.py on the team's GitHub (22 Nov 2026).
AUTH_USER_SQL = '''
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP
)
'''


class AuthContactSchemaTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.execute(AUTH_USER_SQL)
        self.db.executemany(
            'INSERT INTO "User" (UserName, PasswordHash, Email) VALUES (?, ?, ?)',
            [("alice", "hashed-alice", "alice@example.org"),
             ("bob", "hashed-bob", "bob@example.org")],
        )
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_preserves_authentication_schema_and_login_data(self):
        before = [tuple(r) for r in self.db.execute('SELECT * FROM "User" ORDER BY UserID')]
        initialize_contact_tables(self.db)
        after = [tuple(r) for r in self.db.execute('SELECT * FROM "User" ORDER BY UserID')]
        self.assertEqual(before, after)
        self.assertIn("UserID", {r[1] for r in self.db.execute('PRAGMA table_info("User")')})

    def test_contact_and_phone_fk_reference_right_keys(self):
        initialize_contact_tables(self.db)
        fks = [tuple(r) for r in self.db.execute('PRAGMA foreign_key_list("Contact")')]
        self.assertTrue(any(r[2] == "User" and r[3] == "user_id" and r[4] == "UserID" for r in fks))
        self.db.execute(
            'INSERT INTO "Contact" (user_id,full_name,email,address) VALUES (?,?,?,?)',
            (1, "Alice Contact", "", ""),
        )
        self.db.execute(
            'INSERT INTO "Phone_Number" (contact_id,phone_number,label) VALUES (?,?,?)',
            (1, "0901234567", "mobile"),
        )
        self.db.commit()
        self.assertEqual(self.db.execute('SELECT user_id FROM "Contact"').fetchone()[0], 1)
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_unknown_user_id_cannot_be_used(self):
        initialize_contact_tables(self.db)
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                'INSERT INTO "Contact" (user_id,full_name) VALUES (?,?)',
                (999, "Ghost"),
            )
        self.db.rollback()

    def test_deleting_auth_user_cascades_contacts_and_phones(self):
        initialize_contact_tables(self.db)
        self.db.execute('INSERT INTO "Contact" (user_id,full_name) VALUES (?,?)', (1, "A"))
        self.db.execute('INSERT INTO "Phone_Number" (contact_id,phone_number) VALUES (?,?)', (1, "0901234567"))
        self.db.execute('DELETE FROM "User" WHERE UserID = 1')
        self.db.commit()
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "Contact"').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "Phone_Number"').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "User" WHERE UserID = 2').fetchone()[0], 1)

    def test_repeated_schema_initialization_keeps_records(self):
        initialize_contact_tables(self.db)
        self.db.execute('INSERT INTO "Contact" (user_id,full_name) VALUES (?,?)', (1, "Saved"))
        self.db.commit()
        initialize_contact_tables(self.db)
        self.assertEqual(self.db.execute('SELECT full_name FROM "Contact"').fetchone()[0], "Saved")

    def test_rejects_old_demo_user_schema_without_mutating_it(self):
        old = sqlite3.connect(":memory:")
        try:
            old.execute('CREATE TABLE "User" (id INTEGER PRIMARY KEY, username TEXT)')
            with self.assertRaises(SchemaCompatibilityError):
                initialize_contact_tables(old)
            tables = {r[0] for r in old.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertNotIn("Contact", tables)
        finally:
            old.close()

    def test_incompatible_contact_fk_rejected_without_rewrite(self):
        self.db.executescript('''
            CREATE TABLE "Contact" (
                id INTEGER PRIMARY KEY, user_id INTEGER, full_name TEXT, email TEXT, address TEXT,
                FOREIGN KEY (user_id) REFERENCES "User"(id)
            );
            CREATE TABLE "Phone_Number" (
                id INTEGER PRIMARY KEY, contact_id INTEGER, phone_number TEXT, label TEXT,
                FOREIGN KEY (contact_id) REFERENCES "Contact"(id)
            );
        ''')
        with self.assertRaises(SchemaCompatibilityError):
            initialize_contact_tables(self.db)

    def test_group_tables_are_not_created_before_team_approval(self):
        initialize_contact_tables(self.db)
        tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertNotIn("Contact_Group", tables)
        self.assertNotIn("Contact_Group_Member", tables)

    def test_proposed_group_schema_blocks_cross_user_contacts(self):
        initialize_contact_tables(self.db)
        self.db.executescript((ROOT / "database" / "schema_groups_PROPOSED.sql").read_text(encoding="utf-8"))
        self.db.execute('INSERT INTO "Contact" (user_id,full_name) VALUES (1,"A")')
        self.db.execute('INSERT INTO "Contact" (user_id,full_name) VALUES (2,"B")')
        self.db.execute('INSERT INTO "Contact_Group" (user_id,group_name) VALUES (1,"Group")')
        self.db.execute('INSERT INTO "Contact_Group_Member" (group_id,contact_id) VALUES (1,1)')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO "Contact_Group_Member" (group_id,contact_id) VALUES (1,2)')
        self.db.rollback()


if __name__ == "__main__":
    unittest.main()
