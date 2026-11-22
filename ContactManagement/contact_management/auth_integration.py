"""Safely initialize ContactManagement tables alongside the EXISTING Auth schema.

Use the SQLite connection returned by Authentication.database.connection.get_connection().
This function never creates, renames, or changes the Authentication User table.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

_SCHEMA = Path(__file__).resolve().parents[1] / "database" / "schema_auth_contact.sql"
_AUTH_USER_FIELDS = {"UserID", "UserName", "PasswordHash", "Email", "CreatedAt"}
_CONTACT_FIELDS = {"id", "user_id", "full_name", "email", "address"}
_PHONE_FIELDS = {"id", "contact_id", "phone_number", "label"}


class SchemaCompatibilityError(RuntimeError):
    """Database schema conflicts with Authentication's UserID-based schema."""


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f'PRAGMA table_info("{table}")')}


def _foreign_key_exists(
    conn: sqlite3.Connection, table: str, parent: str,
    from_column: str, to_column: str,
) -> bool:
    # pragma fields: id, seq, table, from, to, on_update, on_delete, match
    return any(
        str(row[2]).lower() == parent.lower()
        and str(row[3]).lower() == from_column.lower()
        and str(row[4]).lower() == to_column.lower()
        for row in conn.execute(f'PRAGMA foreign_key_list("{table}")')
    )


def _validate_auth_user(conn: sqlite3.Connection) -> None:
    fields = _columns(conn, "User")
    missing = _AUTH_USER_FIELDS - fields
    if missing:
        raise SchemaCompatibilityError(
            "Expected Authentication.User(UserID, UserName, PasswordHash, Email, "
            "CreatedAt). Missing columns: " + ", ".join(sorted(missing))
            + ". Run Authentication.initialize_database() on the intended DB first; "
            "do not run schema_demo.sql on the production database."
        )
    pk = [row[1] for row in conn.execute('PRAGMA table_info("User")') if row[5] == 1]
    if pk != ["UserID"]:
        raise SchemaCompatibilityError("Authentication.UserID must be the User primary key.")


def _validate_contacts(conn: sqlite3.Connection) -> None:
    if not _CONTACT_FIELDS.issubset(_columns(conn, "Contact")):
        raise SchemaCompatibilityError("Contact must have id, user_id, full_name, email, address.")
    if not _foreign_key_exists(conn, "Contact", "User", "user_id", "UserID"):
        raise SchemaCompatibilityError(
            "Contact.user_id must reference User.UserID. "
            "An old demo Contact -> User.id FK cannot be reused without migration."
        )
    if not _PHONE_FIELDS.issubset(_columns(conn, "Phone_Number")):
        raise SchemaCompatibilityError("Phone_Number must have id, contact_id, phone_number, label.")
    if not _foreign_key_exists(conn, "Phone_Number", "Contact", "contact_id", "id"):
        raise SchemaCompatibilityError("Phone_Number.contact_id must reference Contact.id.")


def initialize_contact_tables(connection: sqlite3.Connection) -> None:
    """Add/verify Contact and Phone_Number without rewriting Auth's User table.

    Requires an open sqlite3 connection with no active transaction. Always run
    Authentication.initialize_database() first and use the SAME phonebook.db.
    Raises SchemaCompatibilityError rather than silently changing legacy tables.
    Group tables are intentionally excluded until Member 3/4 agree on schema.
    """
    if connection.in_transaction:
        raise SchemaCompatibilityError(
            "Commit or roll back the current transaction before schema initialization."
        )
    connection.execute("PRAGMA foreign_keys = ON")
    _validate_auth_user(connection)

    # Fail BEFORE executing CREATE TABLE IF NOT EXISTS if old demo tables exist.
    old_tables = {
        row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    if "Contact" in old_tables or "Phone_Number" in old_tables:
        if not {"Contact", "Phone_Number"}.issubset(old_tables):
            raise SchemaCompatibilityError(
                "Existing Contact/Phone_Number tables are incomplete; back up and review DB."
            )
        _validate_contacts(connection)

    connection.executescript(_SCHEMA.read_text(encoding="utf-8"))
    _validate_contacts(connection)
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        raise SchemaCompatibilityError(
            "Existing foreign-key violations detected; review data migration first: "
            + str(violations[:3])
        )
