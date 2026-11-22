"""Regression checks for Authentication column naming in ALL demo entry points."""
import sqlite3
from contextlib import closing
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from contact_management.auth_integration import initialize_contact_tables
import app_contact_cli

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["UserID", "UserName", "PasswordHash", "Email", "CreatedAt"]


class DemoSchemaAlignmentTests(unittest.TestCase):
    def test_demo_user_has_same_columns_as_authentication(self):
        db = sqlite3.connect(":memory:")
        try:
            db.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
            columns = [r[1] for r in db.execute('PRAGMA table_info("User")')]
            self.assertEqual(columns, EXPECTED)
            fks = db.execute('PRAGMA foreign_key_list("Contact")').fetchall()
            self.assertTrue(any(row[2] == "User" and row[3] == "user_id"
                                and row[4] == "UserID" for row in fks))
        finally:
            db.close()

    def test_auth_contact_initializer_accepts_demo_user_schema(self):
        db = sqlite3.connect(":memory:")
        try:
            db.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
            initialize_contact_tables(db)
        finally:
            db.close()

    def test_cli_initialization_creates_matching_sample_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(app_contact_cli, "DB_FILE", Path(tmp) / "demo_contacts.db"):
                con = app_contact_cli.open_demo_database()
                try:
                    item = con.execute('SELECT UserID, UserName, PasswordHash, Email, CreatedAt '
                                       'FROM "User" WHERE UserID = ?', (1,)).fetchone()
                    self.assertIsNotNone(item)
                    self.assertEqual(item[1], "local_demo_user")
                    self.assertTrue(item[2])
                    self.assertTrue(item[4])
                finally:
                    con.close()

    def test_legacy_demo_db_is_rejected_without_changing_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "demo_contacts.db"
            # sqlite3.Connection used with `with` does NOT close the file handle.
            # close explicitly so TemporaryDirectory can remove it on Windows.
            with closing(sqlite3.connect(path)) as old:
                with old:
                    old.execute('CREATE TABLE "User" (id INTEGER PRIMARY KEY, username TEXT)')
                    old.execute('INSERT INTO "User" VALUES (1, "existing_user")')
            with patch.object(app_contact_cli, "DB_FILE", path):
                with self.assertRaisesRegex(RuntimeError, "Data was NOT changed"):
                    app_contact_cli.open_demo_database()
            with closing(sqlite3.connect(path)) as check:
                self.assertEqual(check.execute('SELECT username FROM "User"').fetchone()[0],
                                 "existing_user")
                self.assertEqual([r[1] for r in check.execute('PRAGMA table_info("User")')],
                                 ["id", "username"])


if __name__ == "__main__":
    unittest.main()
