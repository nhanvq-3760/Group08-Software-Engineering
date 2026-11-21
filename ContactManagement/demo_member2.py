"""Run: python demo_member2.py  (no installation or network required)."""
import sqlite3
from pathlib import Path
from contact_management import ContactService, SQLiteContactRepository


def main() -> None:
    db = sqlite3.connect(":memory:")
    db.executescript(Path("database/schema_demo.sql").read_text(encoding="utf-8"))
    db.execute('INSERT INTO "User"(id, username) VALUES(1, ?)', ("sample_user",))
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
    db.close()


if __name__ == "__main__":
    main()
