# Complete User schema naming alignment (2026-11-22)

## Fixed naming

Authentication's existing SQLite schema is the source of truth:

```sql
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP
);
```

Both the integration schema and **the local test/demo `schema_demo.sql`** now
follow these exact five column names. The `Contact.user_id` column references
`User.UserID`; the `Phone_Number.contact_id` column references `Contact.id`.
These names are intentionally different because they refer to different tables.

## What changed in Member 2's source

- `database/schema_demo.sql`: local `User` now has `UserID`, `UserName`,
  `PasswordHash`, `Email`, `CreatedAt`; `Contact.user_id` FK references `UserID`.
- `demo_member2.py`: inserts sample User with all required User fields.
- `app_contact_cli.py`: likewise inserts sample User with all required fields;
  detects/rejects the old demo DB rather than modifying data.
- `tests/test_contact_management.py`: 24 existing CRUD tests updated to use
  `UserID`/`UserName`/`PasswordHash`/`Email` and delete by `UserID`.
- `tests/test_demo_schema_alignment.py`: 4 extra schema/legacy-protection tests.
- `docs/INTEGRATION_CONTRACT.md` and `README_INTEGRATION.md` updated.

Previous patch files remain valid, especially:

- `contact_management/auth_integration.py`: requires Authentication `User` columns.
- `database/schema_auth_contact.sql`: correct production Contact/Phone FK schema.
- `database/schema_groups_PROPOSED.sql`: **proposal only**, not auto-installed.
- `tests/test_auth_integration.py`: 9 integration tests. **One negative test
  deliberately constructs obsolete `User(id, username)` to verify it is rejected.**
  This is not an active schema definition.

## Applying without damaging existing databases

1. Back up the project and `demo_contacts.db` if it exists. The actual
   Authentication `phonebook.db` must never be overwritten by the demo.
2. Copy the revised Member 2 files over the matching paths in `ContactManagement`.
3. Run `python -m unittest discover -s tests -v` **from `ContactManagement`**.
   Expected: 37 tests = 24 CRUD + 9 integration + 4 demo-schema alignment.
4. Run `python demo_member2.py` to verify the in-memory demo.
5. Before running `python app_contact_cli.py`, check whether the previous
   `demo_contacts.db` was generated with `User(id,username)`.
   If so, **rename it**, e.g. `demo_contacts_legacy_backup.db`, then run the CLI
   to create a new demo DB. Do not delete the backup if you need old contacts.
   There is no automatic migration of old demo contacts in this patch.

## Important limits

Passing the tests demonstrates compatible SQL/table naming **for the modules
under test**, not a completed GUI integration. The group-table SQL remains a
proposal until Members 3 and 4 accept it. The Authentication User table is
unchanged and is still owned by Member 1.
