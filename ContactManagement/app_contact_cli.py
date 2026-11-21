"""Optional standalone CLI for demoing all 5 Member-2 CRUD features.

Runs with a LOCAL SAMPLE USER only, NOT real login/authentication.
Usage: python app_contact_cli.py
"""
import sqlite3
from pathlib import Path
from contact_management import ContactService, SQLiteContactRepository
from contact_management.models import ContactNotFound, ContactValidationError

ROOT = Path(__file__).resolve().parent
DB_FILE = ROOT / "demo_contacts.db"
USER_ID = 1  # local demonstration account; production MUST use Member-1 session!


def open_demo_database():
    con = sqlite3.connect(DB_FILE)
    con.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
    con.execute('INSERT OR IGNORE INTO "User" (id, username) VALUES (?, ?)',
                (USER_ID, "local_demo_user"))
    con.commit()
    return con


def render(contacts):
    if not contacts:
        print("No contacts found.")
    for c in contacts:
        print(f"#{c.id} | {c.full_name} | {c.email or '-'} | "
              f"{', '.join(c.phone_numbers) or '-'} | {c.address or '-'}")


def main():
    con = open_demo_database()
    service = ContactService(SQLiteContactRepository(con))
    try:
        while True:
            print("\nCONTACT MANAGEMENT - Member 2 (local demo)")
            print("1 Add | 2 View | 3 Search | 4 Update | 5 Delete | 0 Exit")
            choice = input("Choose: ").strip()
            try:
                if choice == "0":
                    break
                if choice == "1":
                    name = input("Full name: ")
                    email = input("Email (optional): ")
                    phone = input("Phone (optional): ")
                    address = input("Address (optional): ")
                    c = service.add_contact(USER_ID, name, email=email,
                                            address=address,
                                            phone_numbers=[phone] if phone.strip() else [])
                    print("Added contact #", c.id)
                elif choice == "2":
                    render(service.view_contacts(USER_ID))
                elif choice == "3":
                    render(service.search_contacts(USER_ID, input("Search: ")))
                elif choice == "4":
                    contact_id = int(input("Contact ID: "))
                    old = service.view_contact(USER_ID, contact_id)
                    print("Enter new name (leave empty to keep current):", old.full_name)
                    name = input("New name: ")
                    c = service.update_contact(USER_ID, contact_id,
                                               **({"full_name": name} if name.strip() else {}))
                    print("Updated:")
                    render([c])
                elif choice == "5":
                    contact_id = int(input("Contact ID: "))
                    service.delete_contact(USER_ID, contact_id)
                    print("Deleted contact #", contact_id)
                else:
                    print("Unknown choice")
            except (ContactNotFound, ContactValidationError, ValueError) as exc:
                print("ERROR:", exc)
    except (KeyboardInterrupt, EOFError):
        print("\nDemo ended.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
