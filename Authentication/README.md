# Phone Book Management System – Member 1

## Responsibilities
- Layered project structure and application entry point
- User registration
- Login and logout
- Update profile
- Initial SQLite database setup
- Authentication unit tests
- Git/GitHub integration coordination

## Requirements
- Python 3.10+
- pytest

## Run
```bash
python main.py
```

The SQLite database is created automatically as `phonebook.db` on first run.

## Test
Install pytest and run:
```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

## Architecture
- `presentation/`: Tkinter screens
- `business/`: authentication and profile rules
- `data_access/`: SQL queries/repository
- `database/`: SQLite connection and schema
- `tests/`: unit tests

## Integration contract for teammates
- Use `database.connection.get_connection()` to get a SQLite connection.
- Keep database queries in `data_access/`.
- Put validation and business rules in `business/`.
- Do not write SQL directly inside Tkinter screens.
- Contact and group modules should use `UserID` as the owner foreign key.
- Coordinate schema changes with the team before merging.

## Security
Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, not plaintext.
SQL statements use parameterized placeholders.
