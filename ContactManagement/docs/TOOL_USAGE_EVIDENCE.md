# Tool Usage Evidence — Member 2

## Tools actually used to create and verify this submission

**Python interpreter + unittest:** the following command was executed from the project root:

```bash
python -m unittest discover -s tests -v
```

The complete actual output and runtime are recorded in `TEST_RESULTS.txt`. All test cases run on an in-memory SQLite database. This is genuine command-output evidence; no fake screenshot is included.

**SQLite (`sqlite3`, Python standard library):** `database/schema_demo.sql` creates the three necessary demo tables and enforces foreign keys, which are tested by TC08, TC15 and TC23. SQL queries are parameterized (TC16).

**Docker:** `Dockerfile` is provided for reproducible execution of the test suite:

```powershell
docker build -t member2-contact-tests .
docker run --rm member2-contact-tests
```

Docker was **not run** in this environment, so its output is not claimed. Run it and save a screenshot/log if your instructor requires Docker execution evidence.

## Task assignment evidence

`TASK_ASSIGNMENT.md` records all four members' assigned Stage 3 and Stage 4 responsibilities, using exactly the task split provided. Replace `XY` with your group number and fill real member names before submission.

## Screenshots recommended for final submission (not fabricated)

1. VS Code showing `contact_management/service.py`.
2. PowerShell showing `python -m unittest discover -s tests -v` with `OK`.
3. `python app_contact_cli.py` demonstrating add/view/search/update/delete.
4. Docker test output after running on a computer with Docker installed.

Keep screenshots inside a `docs/evidence/` folder only if you actually capture them.
