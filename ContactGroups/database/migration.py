import sqlite3
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parent / "schema_contact_groups.sql"


def initialize_contact_group_tables(connection):
    if connection.in_transaction:
        raise RuntimeError("Cannot initialize Contact Groups during an active transaction.")

    connection.execute("PRAGMA foreign_keys = ON")

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)

    foreign_key_errors = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if foreign_key_errors:
        raise RuntimeError(
            f"Contact Groups foreign key validation failed: {foreign_key_errors}"
        )
