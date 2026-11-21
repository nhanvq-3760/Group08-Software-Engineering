# ProgAndTest_GroupXY — Stage 3 & Stage 4 (Member 2)

## Contact Management Module

**Status:** Member 2 source code + automated tests completed in a standalone demo.
**Important:** This does **not** mean the four members' modules are integrated yet.
**Language:** Python 3.10+ (`sqlite3`, `unittest` — no third-party dependencies).

### Five implemented features

1. **Add Contact:** name, optional email/address, multiple phone numbers.
2. **View Contacts:** list contacts belonging to the authenticated user.
3. **Search Contact:** case-insensitive Vietnamese name, phone, email or address.
4. **Update Contact:** modify name/email/address/phone numbers.
5. **Delete Contact:** remove contact; phone records deleted by FK cascade.

Data validation and ownership checks prevent one user from viewing or changing another user's contacts.

### Quick start on Windows PowerShell

```powershell
cd "C:\path\to\ProgAndTest_GroupXY"
python --version
python -m unittest discover -s tests -v
python demo_member2.py
python app_contact_cli.py
```

`demo_member2.py` runs the five CRUD functions once, in memory. `app_contact_cli.py` is a simple interactive test app that keeps **sample** records in `demo_contacts.db` (not production data). It is for Member 2's local demo; it is **not an authenticated multi-user web application**.

### Run tests in Docker

```powershell
docker build -t member2-contact-tests .
docker run --rm member2-contact-tests
```

Docker runs the same Python unit tests and does not deploy the team application. Requires Docker Desktop installed on Windows.

### Code layout

```text
ProgAndTest_GroupXY/
  contact_management/
    __init__.py
    models.py              # Domain contact types/errors
    contracts.py           # Repository interface
    service.py             # Add / View / Search / Update / Delete logic
    sqlite_repository.py   # SQL queries for Contact + Phone_Number
    controller.py          # Entry points called by Member 1 after login
  database/schema_demo.sql # TEST/DEMO ONLY; Member 4 owns production tables
  tests/test_contact_management.py
  docs/TESTING_DOCUMENT.md
  docs/TEST_RESULTS.txt
  docs/TOOL_USAGE_EVIDENCE.md
  docs/TASK_ASSIGNMENT.md
  docs/INTEGRATION_CONTRACT.md
  app_contact_cli.py
  demo_member2.py
  Dockerfile
  .dockerignore
```

### Integration boundaries

- **Member 1**: provides valid `authenticated_user_id` after Register/Login; calls `ContactController`. Contact Management does not implement login itself.
- **Member 4**: provides DB connection and the `User`, `Contact`, `Phone_Number` table structures (plus both group tables). Align column names in `docs/INTEGRATION_CONTRACT.md` before merging.
- **Member 3**: stores `contact_id` values in `Contact_Group_Member` and handles the UI for contact groups.

Refer to `docs/INTEGRATION_CONTRACT.md` for example integration and endpoints.

### What was verified

The Python unit/integration suite covers CRUD, user isolation, bad inputs, phone relationships, and SQL injection handling. Results are captured in `docs/TEST_RESULTS.txt`. **Docker build and integration with the full team's source were not run in this environment.**
