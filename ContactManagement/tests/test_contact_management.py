"""Member 2 unit + SQLite integration tests (no external dependencies).

Local User fixtures now use the exact Authentication User column names.
"""
import sqlite3
import unittest
from pathlib import Path
from contact_management import (
    ContactService, SQLiteContactRepository, ContactController,
    ContactNotFound, ContactValidationError,
)

ROOT = Path(__file__).resolve().parents[1]


class ContactManagementTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
        self.db.executemany(
            'INSERT INTO "User" (UserID, UserName, PasswordHash, Email) VALUES (?, ?, ?, ?)',
            [(1, "alice", "TEST_ONLY_HASH_ALICE", "alice@example.invalid"),
             (2, "bob", "TEST_ONLY_HASH_BOB", "bob@example.invalid")],
        )
        self.db.commit()
        self.service = ContactService(SQLiteContactRepository(self.db))
        self.controller = ContactController(self.service)

    def tearDown(self):
        self.db.close()

    def add(self, user_id=1, name="Nguyễn Văn An"):
        return self.service.add_contact(user_id, name,
                                        email="an@example.com", phone_numbers=["0901234567"])

    def test_01_add_contact_and_return_id(self):
        c = self.add()
        self.assertIsInstance(c.id, int)
        self.assertEqual(c.full_name, "Nguyễn Văn An")
        self.assertEqual(c.phone_numbers, ("0901234567",))

    def test_02_view_contacts_only_current_user(self):
        self.add(1)
        self.add(2, "Trần Thị Bình")
        self.assertEqual(len(self.service.view_contacts(1)), 1)
        self.assertEqual(len(self.service.view_contacts(2)), 1)
        self.assertEqual(self.service.view_contacts(2)[0].full_name, "Trần Thị Bình")

    def test_03_view_single_contact(self):
        c = self.add()
        self.assertEqual(self.service.view_contact(1, c.id), c)

    def test_04_search_by_unicode_name(self):
        self.add(name="Đỗ Thị Ánh")
        self.assertEqual(len(self.service.search_contacts(1, "đỗ")), 1)
        self.assertEqual(len(self.service.search_contacts(1, "ÁNH")), 1)

    def test_05_search_by_phone_email_and_address(self):
        c = self.service.add_contact(1, "Minh", email="minh@example.org",
                                     address="Quận 3", phone_numbers=["0912345678"])
        for q in ["minh@", "091234", "quận 3"]:
            self.assertEqual([x.id for x in self.service.search_contacts(1, q)], [c.id])

    def test_06_update_contact_properties(self):
        c = self.add()
        c2 = self.service.update_contact(1, c.id, full_name="Nguyễn Văn An B",
                                          email="", address="HCMC")
        self.assertEqual(c2.id, c.id)
        self.assertEqual(c2.full_name, "Nguyễn Văn An B")
        self.assertEqual(c2.email, "")
        self.assertEqual(c2.address, "HCMC")
        self.assertEqual(c2.phone_numbers, ("0901234567",))

    def test_07_update_and_clear_phone_numbers(self):
        c = self.add()
        updated = self.service.update_contact(1, c.id,
                                               phone_numbers=["0901234567", "+84 912 345 678"])
        self.assertEqual(len(updated.phone_numbers), 2)
        cleared = self.service.update_contact(1, c.id, phone_numbers=[])
        self.assertEqual(cleared.phone_numbers, ())

    def test_08_delete_removes_contact_and_phone_rows(self):
        c = self.add()
        self.service.delete_contact(1, c.id)
        self.assertEqual(self.service.view_contacts(1), [])
        count = self.db.execute('SELECT COUNT(*) FROM "Phone_Number" WHERE contact_id = ?',
                                (c.id,)).fetchone()[0]
        self.assertEqual(count, 0)

    def test_09_users_cannot_view_another_users_contact(self):
        c = self.add(1)
        with self.assertRaises(ContactNotFound):
            self.service.view_contact(2, c.id)

    def test_10_users_cannot_update_another_users_contact(self):
        c = self.add(1)
        with self.assertRaises(ContactNotFound):
            self.service.update_contact(2, c.id, full_name="Changed")
        self.assertEqual(self.service.view_contact(1, c.id).full_name, "Nguyễn Văn An")

    def test_11_users_cannot_delete_another_users_contact(self):
        c = self.add(1)
        with self.assertRaises(ContactNotFound):
            self.service.delete_contact(2, c.id)
        self.assertEqual(len(self.service.view_contacts(1)), 1)

    def test_12_reject_blank_name(self):
        with self.assertRaises(ContactValidationError):
            self.service.add_contact(1, "  ")

    def test_13_reject_invalid_email(self):
        with self.assertRaises(ContactValidationError):
            self.service.add_contact(1, "Test", email="invalid-email")

    def test_14_reject_invalid_phones_and_duplicates(self):
        for bad in (["abc"], ["123"], ["0912345678", "0912345678"]):
            with self.subTest(phone_numbers=bad), self.assertRaises(ContactValidationError):
                self.service.add_contact(1, "Test", phone_numbers=bad)

    def test_15_reject_missing_user_record(self):
        with self.assertRaises(ContactValidationError):
            self.service.add_contact(9999, "Test")

    def test_16_sql_injection_does_not_modify_database(self):
        self.service.add_contact(1, "Robert'); DROP TABLE Contact;--")
        self.assertEqual(len(self.service.view_contacts(1)), 1)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "Contact"').fetchone()[0], 1)

    def test_17_nonexistent_contact_raises(self):
        with self.assertRaises(ContactNotFound):
            self.service.delete_contact(1, 1000)

    def test_18_reject_invalid_user_and_contact_identifiers(self):
        for invalid in (0, -1, True, "1"):
            with self.subTest(value=invalid), self.assertRaises(ContactValidationError):
                self.service.view_contacts(invalid)
        with self.assertRaises(ContactValidationError):
            self.service.view_contact(1, -1)

    def test_19_controller_crud_without_client_chosen_user_id(self):
        # Client-supplied user_id=2 must not override authenticated_user_id=1.
        item = self.controller.add(1, {"user_id": 2, "full_name": "Lan",
                                       "phone_numbers": ["0901234567"]})
        self.assertEqual(item["user_id"], 1)
        self.assertEqual(len(self.controller.list(2)), 0)
        self.assertEqual(len(self.controller.search(1, "Lan")), 1)
        edited = self.controller.edit(1, item["id"], {"full_name": "Lan A"})
        self.assertEqual(edited["full_name"], "Lan A")
        self.assertTrue(self.controller.remove(1, item["id"])["deleted"])

    def test_20_data_isolation_on_search(self):
        self.add(1, "Unique Private Person")
        self.assertEqual(self.service.search_contacts(2, "Private"), [])

    def test_21_empty_query_lists_all_current_users_contacts(self):
        self.add(1, "An")
        self.add(1, "Bình")
        self.assertEqual(len(self.service.search_contacts(1, " ")), 2)

    def test_22_phone_data_transaction_rollback_on_invalid_duplicate(self):
        # Database constraint violation inside a transaction must not leave partial rows.
        c = self.add()
        with self.assertRaises(ContactValidationError):
            self.service.add_contact(1, "New", phone_numbers=["0901234567", "0901234567"])
        self.assertEqual(len(self.service.view_contacts(1)), 1)
        self.assertEqual(self.service.view_contact(1, c.id).phone_numbers, ("0901234567",))

    def test_23_delete_user_cascades_contacts(self):
        self.add(1)
        self.db.execute('DELETE FROM "User" WHERE UserID = 1')
        self.db.commit()
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "Contact"').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM "Phone_Number"').fetchone()[0], 0)

    def test_24_search_does_not_match_other_contacts(self):
        self.add(1, "Nguyễn Văn An")
        self.add(1, "Trần Thị Bình")
        self.assertEqual(len(self.service.search_contacts(1, "ZZZZ-no-results")), 0)


if __name__ == "__main__":
    unittest.main()
