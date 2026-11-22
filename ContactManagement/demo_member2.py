"""Run: python demo_member2.py (standalone in-memory CRUD demonstration).

User column names match Authentication's real SQLite schema.
The demo user has a placeholder PasswordHash; it is NOT a login account.
"""
import sqlite3
from pathlib import Path
from contact_management import ContactService, SQLiteContactRepository

ROOT = Path(__file__).resolve().parent


def main() -> None:
    db = sqlite3.connect(":memory:")
    try:
        db.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
        db.execute(
            'INSERT INTO "User" (UserID, UserName, PasswordHash, Email) VALUES (?, ?, ?, ?)',
            (1, "sample_user", "DEMO_ONLY_NOT_VALID_LOGIN_HASH", "sample@example.invalid"),
        )
        db.commit()
        service = ContactService(SQLiteContactRepository(db))
        c = service.add_contact(1, "Nguyễn Văn An", email="an@example.com",
                                phone_numbers=["0901234567"])
        print("ADD:", c.to_dict())
        print("VIEW:", [x.to_dict() for x in service.view_contacts(1)])
        print("SEARCH:", [x.to_dict() for x in service.search_contacts(1, "An")])
        c = service.update_contact(1, c.id, full_name="Nguyễn Văn An Updated",
                                   phone_numbers=["0901234567", "+84 912 345 678"])
        print("UPDATE:", c.to_dict())
        service.delete_contact(1, c.id)
        print("DELETE: successful; remaining", len(service.view_contacts(1)))
    finally:
        db.close()


if __name__ == "__main__":
    main()
