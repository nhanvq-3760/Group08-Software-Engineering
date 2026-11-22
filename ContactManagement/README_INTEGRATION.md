# Contact Management — Authentication UserID-aligned code update

The existing Authentication table is kept **unchanged**:

`User(UserID, UserName, PasswordHash, Email, CreatedAt)`

Contact Management now uses these same five `User` column names in the local
demo database, CLI, 24 unit tests and integration checks. Contact and Phone
keys remain `Contact.id`, `Contact.user_id`, `Phone_Number.id` and
`Phone_Number.contact_id`; `Contact.user_id` references `User.UserID`.

## Apply the update to the existing team repository

This zip is an **overlay**, not a replacement for the whole project. Extract it
into the repository root, preserving the `ContactManagement/...` paths. It will
replace the relevant existing demo, test and documentation files. Keep the
previous patch's `auth_integration.py`, `schema_auth_contact.sql`,
`schema_groups_PROPOSED.sql`, and `test_auth_integration.py`.

**Back up `demo_contacts.db` and `Authentication/phonebook.db` before updating**.
The demo CLI refuses an incompatible old demo database without mutating it.
For a new demo database, rename old `demo_contacts.db` to
`demo_contacts_legacy_backup.db` (do not delete it).

```powershell
cd ContactManagement
python -m unittest discover -s tests -v
python demo_member2.py
python app_contact_cli.py
```

Expected automated tests: **37** (24 CRUD, 9 Authentication integration,
4 extra demo schema checks). These tests were executed on the module source
with the updated patch; repeat in your local Git checkout before pushing.

See `docs/SCHEMA_ALIGNMENT.md` and `docs/INTEGRATION_CONTRACT.md`.

**Not included:** modifying Authentication, actual migrations of old contact
data, finalized contact-group schema (Member 3/4 approval required), and GUI wiring.
