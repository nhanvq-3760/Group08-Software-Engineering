"""Standalone Contact Management CLI using a LOCAL SAMPLE USER, not real login.

Run: python app_contact_cli.py
This demo's User schema matches Authentication (UserID, UserName, PasswordHash,
Email, CreatedAt), but uses a placeholder hash and local-only demo database.
"""
import sqlite3
from pathlib import Path
from contact_management import ContactService, SQLiteContactRepository
from contact_management.models import ContactNotFound, ContactValidationError

ROOT = Path(__file__).resolve().parent
DB_FILE = ROOT / "demo_contacts.db"
USER_ID = 1  # Local demo only; a real app MUST use the verified Authentication session.
EXPECTED_USER_COLUMNS = {"UserID", "UserName", "PasswordHash", "Email", "CreatedAt"}


def _check_existing_schema(con: sqlite3.Connection) -> None:
    """Reject a legacy demo database without modifying or deleting its rows."""
    table_names = {
        row[0] for row in con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    if "User" not in table_names:
        if "Contact" in table_names or "Phone_Number" in table_names:
            raise RuntimeError("Incomplete old demo database: back up demo_contacts.db and review it.")
        return
    cols = {row[1] for row in con.execute('PRAGMA table_info("User")')}
    if cols != EXPECTED_USER_COLUMNS:
        raise RuntimeError(
            "Old demo_contacts.db schema found: expected UserID, UserName, "
            "PasswordHash, Email, CreatedAt. Data was NOT changed. Back up or "
            "rename demo_contacts.db, then run the CLI again to create a fresh demo DB."
        )
    if "Contact" in table_names:
        fk = con.execute('PRAGMA foreign_key_list("Contact")').fetchall()
        if not any(str(row[2]).lower() == "user" and row[3] == "user_id"
                   and row[4] == "UserID" for row in fk):
            raise RuntimeError(
                "Old Contact foreign key found. Data was NOT changed; "
                "back up demo_contacts.db and review migration before continuing."
            )
    if ("Contact" in table_names) != ("Phone_Number" in table_names):
        raise RuntimeError("Incomplete demo database: back up demo_contacts.db and review it.")


def open_demo_database():
    con = sqlite3.connect(DB_FILE)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        _check_existing_schema(con)
        con.executescript((ROOT / "database" / "schema_demo.sql").read_text(encoding="utf-8"))
        con.execute(
            'INSERT OR IGNORE INTO "User" (UserID, UserName, PasswordHash, Email) '
            'VALUES (?, ?, ?, ?)',
            (USER_ID, "local_demo_user", "DEMO_ONLY_NOT_VALID_LOGIN_HASH",
             "local_demo@example.invalid"),
        )
        con.commit()
        return con
    except Exception:
        con.close()
        raise


def render(contacts):
    if not contacts:
        print("No contacts found.")
    for c in contacts:
        print(f"#{c.id} | {c.full_name} | {c.email or '-'} | "
              f"{', '.join(c.phone_numbers) or '-'} | {c.address or '-'}")


def main():
    try:
        con = open_demo_database()
    except (RuntimeError, sqlite3.DatabaseError) as exc:
        print("Cannot start demo:", exc)
        return
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
