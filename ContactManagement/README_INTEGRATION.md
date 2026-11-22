# Integration patch: Authentication UserID + Contact Management

This archive contains only **new files**, to place into the existing `Group08-Software-Engineering` repository. It does **not** replace Authentication, existing CRUD code, existing demo schema, or tests.

## Install
1. Back up the repository and any `Authentication/phonebook.db` file.
2. Extract the archive into the root of the team's repo, preserving `ContactManagement/...` paths.
3. From the `ContactManagement` folder, run `python -m unittest discover -s tests -v`.
4. Read `docs/SCHEMA_ALIGNMENT.md` before using a shared DB.

## Included new files
- `database/schema_auth_contact.sql` — proper FK `Contact.user_id → User.UserID`.
- `contact_management/auth_integration.py` — validates Authentication schema and initializes Contact/Phone safely.
- `tests/test_auth_integration.py` — SQLite compatibility, foreign key, cascade and collision tests.
- `database/schema_groups_PROPOSED.sql` — **not yet approved**, proposed draft for Member 3/4.
- `docs/SCHEMA_ALIGNMENT.md` — setup and agreement points.

## Important
This patch doesn't claim the 4 team modules are fully integrated. GUI wiring and the final group schema remain decisions for the team.
