# Member 2 integration contract — aligned with Authentication UserID

## Team database convention

The **existing Authentication module** owns the SQLite `User` table in
`Authentication/phonebook.db`. Its columns must remain exactly:

`User(UserID, UserName, PasswordHash, Email, CreatedAt)`

`UserID` is the primary key. Do **not** rename `UserID` to `id`, and do **not**
create another `User` table when running against the real Authentication DB.

| Table | Columns | Foreign key |
|---|---|---|
| `User` | `UserID` PK, `UserName`, `PasswordHash`, `Email`, `CreatedAt` | Owned by Authentication |
| `Contact` | `id` PK, `user_id`, `full_name`, `email`, `address` | `Contact.user_id → User.UserID` |
| `Phone_Number` | `id` PK, `contact_id`, `phone_number`, `label` | `Phone_Number.contact_id → Contact.id` (`ON DELETE CASCADE`) |
| `Contact_Group` | **Proposed** `id`, `user_id`, `group_name` | Proposed `user_id → User.UserID`; Member 3/4 must approve |
| `Contact_Group_Member` | **Proposed** `group_id`, `contact_id` | Proposed FKs to `Contact_Group.id` and `Contact.id`; Member 3/4 must approve |

**Important distinction:** `UserID` is a column **only of the `User` table**.
`Contact.id`, `Contact.user_id`, `Phone_Number.id` and `Phone_Number.contact_id`
are intentionally unchanged. The foreign key column does not have to share
its name with its referenced primary key.

## How to initialize the production SQLite tables

Run from the repository root in a correctly configured Python import context:

```python
from Authentication.database.connection import initialize_database, get_connection
from ContactManagement.contact_management.auth_integration import initialize_contact_tables
from ContactManagement.contact_management import ContactController, ContactService, SQLiteContactRepository

initialize_database()  # Existing Authentication User table, not recreated by Contact Management
conn = get_connection()  # Opens Authentication/phonebook.db with FKs enabled
initialize_contact_tables(conn)
controller = ContactController(ContactService(SQLiteContactRepository(conn)))

# ONLY after a verified login:
# verified_user_id = auth_service.current_user["user_id"]
# controller.list(verified_user_id)
```

Note: The team's Authentication code currently uses top-level imports such as
`from data_access.user_repository import UserRepository`. For the final GUI
integration, Member 1 may need to adjust Python package imports. This schema
patch does **not** wire the two GUIs together.

The standalone demo uses a **different** `demo_contacts.db` database, while
`database/schema_demo.sql` now has exactly the same five `User` column names as
Authentication. Demo passwords are placeholders; demo users are not legitimate
login accounts. Never point the demo launcher to `Authentication/phonebook.db`.

## Layered integration

`GUI (Member 1/3) → ContactController → ContactService → SQLiteContactRepository`

The controller takes a verified `authenticated_user_id` from the login session.
It must **never** accept an arbitrary client-provided `user_id` as proof of identity.

Existing Controller API:

```python
new_contact = controller.add(verified_user_id, {
    "full_name": "Nguyễn Văn An", "email": "an@example.com",
    "phone_numbers": ["0901234567"]
})
all_contacts = controller.list(verified_user_id)
found = controller.search(verified_user_id, "An")
controller.edit(verified_user_id, new_contact["id"], {"email": "other@example.com"})
controller.remove(verified_user_id, new_contact["id"])
```

## Unresolved production decisions

- The current code uses SQLite; the team must confirm the final production DB choice.
- Member 3 and Member 4 must approve final group tables and cascades before deployment.
- The application UI/session connection is not integrated merely because tests pass.
- Back up real database files before a production schema change.
- Legacy `User(id, username)` databases are deliberately **rejected** by the
  initializer rather than silently renamed, because migrations risk data loss.
