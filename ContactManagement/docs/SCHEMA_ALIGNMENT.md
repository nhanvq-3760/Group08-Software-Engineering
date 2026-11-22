# Align ContactManagement with Authentication (proposed integration)

**Source of truth, checked 2026-11-22:** `Authentication/database/connection.py` in the team's GitHub repository. Authentication uses **SQLite** in `Authentication/phonebook.db` and creates:

```sql
User(UserID INTEGER PRIMARY KEY AUTOINCREMENT,
     UserName TEXT UNIQUE, PasswordHash TEXT, Email TEXT UNIQUE,
     CreatedAt TEXT)
```

**Keep `User.UserID`**. Do not rename Authentication's columns and do not deploy Member 2's `database/schema_demo.sql` against the Authentication database. That SQL uses `User(id,username)` for isolated tests only.

## Correct integration contract

| Table | Columns / keys | Status |
|---|---|---|
| `User` | `UserID` PK, `UserName`, `PasswordHash`, `Email`, `CreatedAt` | Already owned/created by Authentication |
| `Contact` | `id` PK, `user_id` FK **to `User.UserID`**, `full_name`, `email`, `address` | Added by `schema_auth_contact.sql` |
| `Phone_Number` | `id` PK, `contact_id` FK to `Contact.id`, `phone_number`, `label` | Added by `schema_auth_contact.sql` |
| `Contact_Group` | Proposed `id`, `user_id` FK to `User.UserID`, `group_name` | **Not approved**: Member 3/4 must confirm |
| `Contact_Group_Member` | Proposed `(group_id, contact_id)` PK/FKs | **Not approved**: Member 3/4 must confirm |

`database/schema_groups_PROPOSED.sql` is a **draft** for Members 3/4; it is never loaded automatically. It includes a trigger preventing a user's group from containing another user's contacts.

## Initialize against the SAME SQLite connection

From the **repository root** (`Group08-Software-Engineering`), initialize the Authentication-owned database once, then open that same DB and add the Contact tables:

```python
from Authentication.database.connection import initialize_database, get_connection
from ContactManagement.contact_management.auth_integration import initialize_contact_tables
from ContactManagement.contact_management import ContactService, SQLiteContactRepository, ContactController

initialize_database()  # Creates/retains Authentication/phonebook.db and User(UserID,...)
connection = get_connection()
initialize_contact_tables(connection)
controller = ContactController(ContactService(SQLiteContactRepository(connection)))

# On successful AUTHENTICATED login, use the trusted user ID:
# verified_user_id = auth_service.current_user["user_id"]
# controller.list(verified_user_id)
# controller.add(verified_user_id, {"full_name": "An", "phone_numbers": [...]})
# Close connection at app shutdown; use per-request connections if deployed as a server.
```

**Security:** Never accept `user_id` from the frontend as authentication. Pass only the verified `current_user["user_id"]` returned by `AuthService.login` / the server session.

## Running tests (does not touch real user data)

```powershell
cd Group08-Software-Engineering\ContactManagement
python -m unittest discover -s tests -v
```

Existing `demo_member2.py` and `app_contact_cli.py` continue to use **the demo SQLite database** and demo `User(id,username)`. This is intentional so the 24 pre-existing standalone tests do not break. The new `test_auth_integration.py` specifically verifies the real Authentication schema and the Contact/Phone FKs in memory.

## Migration / ownership warning

- **Backup** `Authentication/phonebook.db` before modifying a real group database.
- If `User(id,username)` or `Contact.user_id -> User.id` already exists in that database, `initialize_contact_tables()` raises `SchemaCompatibilityError`. It **does not** rename or destroy data automatically. Agree on a migration with Member 4.
- The choice of SQLite is grounded in the *currently implemented Authentication module*, not an independent final decision by the whole team.
- No integrated production schema for all five tables existed in the repository before this patch. The group tables are still pending approval from Members 3/4.
- Authentication GUI isn't automatically integrated; its UI must call the contact controller after login and share the verified user ID.
