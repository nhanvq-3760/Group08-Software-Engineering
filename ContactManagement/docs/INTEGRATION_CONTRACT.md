# Member 2 integration contract

## Layered design

`UI / API (Member 1, 3) -> ContactController -> ContactService -> ContactRepository -> SQLite/database (Member 4)`

- Business logic does not import FastAPI, Flask, Tkinter, etc.
- `ContactRepository` is replaceable if Member 4 uses MySQL, PostgreSQL or another DB.
- All queries use parameters, not concatenated user input.

## Required database contract — confirm with Member 4

| Table | Required columns | Relation |
|---|---|---|
| `User` | `id` PK | Main login/user table owned by Member 4 |
| `Contact` | `id` PK, `user_id` FK, `full_name`, `email`, `address` | `Contact.user_id -> User.id` |
| `Phone_Number` | `id` PK, `contact_id` FK, `phone_number`, `label` | `Phone_Number.contact_id -> Contact.id`, ON DELETE CASCADE |
| `Contact_Group` | Defined by Member 3/4 | Groups created by Member 3 |
| `Contact_Group_Member` | `group_id`, `contact_id` FK | Refers to `Contact.id` |

The provided `database/schema_demo.sql` is **only** for Member 2 local tests; do not replace the production DB with this file. In production, when a contact is deleted, Member 4 must also define how related `Contact_Group_Member` rows are handled (typically FK ON DELETE CASCADE).

## Example Member 1 integration

```python
import sqlite3
from contact_management import ContactService, SQLiteContactRepository, ContactController

connection = sqlite3.connect("team_database.db")
controller = ContactController(ContactService(SQLiteContactRepository(connection)))

# IMPORTANT: verified_user_id comes from your REAL login/session middleware.
# Never take it from a client-submitted JSON field.
verified_user_id = session_user_id  # assigned by Member 1's auth implementation
new_contact = controller.add(verified_user_id, {
    "full_name": "Nguyễn Văn An",
    "email": "an@example.com",
    "phone_numbers": ["0901234567"]
})
contacts = controller.list(verified_user_id)
result = controller.search(verified_user_id, "An")
controller.edit(verified_user_id, new_contact["id"], {"email": "new@example.com"})
controller.remove(verified_user_id, new_contact["id"])
```

## Suggested REST endpoints (Member 1 builds routing)

| HTTP | URL | Controller operation |
|---|---|---|
| POST | `/contacts` | `add(current_user_id, payload)` |
| GET | `/contacts` | `list(current_user_id)` |
| GET | `/contacts?q=An` | `search(current_user_id, query)` |
| GET | `/contacts/{id}` | `view(current_user_id, id)` |
| PUT/PATCH | `/contacts/{id}` | `edit(current_user_id, id, payload)` |
| DELETE | `/contacts/{id}` | `remove(current_user_id, id)` |

Map `ContactValidationError` to HTTP 400/422 and `ContactNotFound` to HTTP 404. A real web server must manage DB connections per request and validate authentication, cookies/tokens, CSRF, etc.

## Agree on these questions before merge

1. Is backend Python? If Java/C++ is chosen by Member 1, reimplement or expose this Python module through a service/API.
2. Is production database SQLite, MySQL or PostgreSQL? Adjust repository SQL as needed.
3. Is one contact permitted to have multiple numbers? This module supports 0–10 numbers.
4. Should contacts have an `email`, `address`, soft-delete, or extra columns? Align schema.
5. When a contact is deleted, should Member 3's group membership be cascaded or restricted? Agree with Member 4.
