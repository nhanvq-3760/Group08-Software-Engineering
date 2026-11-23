# Phone Book Management System — Member 4

## Stack
- Python 3
- Tkinter GUI
- SQLite database
- pytest
- Git & GitHub
- Docker

## Included
- `database.py`: creates the five required tables and enables foreign keys.
- `admin_service.py`: lists, creates, activates/deactivates, changes role, and deletes accounts.
- `admin_gui.py`: basic Admin user-management interface.
- `security.py`: PBKDF2-SHA256 password hashing and verification.
- `tests/`: database, integrity, security, and Admin tests.

## Run locally
1. Install Python 3.10+.
2. Install test dependency: `pip install -r requirements.txt`.
3. Initialize database:
   `python -c "from database import initialize_database; initialize_database()"`
4. Connect this module to the group's login flow. After successful login, verify the logged-in user's role is `admin`, then call:
   `open_admin_window(DB_PATH, admin_id)` from `admin_gui.py`.
5. Run tests: `python -m pytest -q`.

## Git / GitHub
```bash
git init
git add .
git commit -m "Add Member 4 database and admin module"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```
Do not commit real user data, passwords, `.env` files, or the generated `.db` file.

## Docker
Build: `docker build -t phonebook-member4 .`
Run GUI: Docker containers need desktop display forwarding; this Dockerfile is a starter and GUI display configuration depends on Windows/macOS/Linux. For CI testing, run:
`docker run --rm phonebook-member4 python -m pytest -q`

## Important integration notes
- This is a starter implementation based on the five table names in the assignment.
- Confirm column names, class names, and relationships against Stage 1 Class Diagram and the group's existing code before merging.
- The Admin GUI currently assumes the authentication module passes a verified `admin_id`. Do not expose Admin screens to ordinary users.
- `delete_user` cascades to that user's contacts and groups. Confirm this deletion policy with the group/lecturer.
