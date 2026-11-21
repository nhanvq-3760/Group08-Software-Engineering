"""SQLite adapter. Member 4 owns production database setup and migrations.

Requires the User, Contact and Phone_Number tables defined in
`database/schema_demo.sql` (demo/testing) or equivalent production tables.
"""
import sqlite3
from .models import Contact, ContactNotFound, ContactValidationError


class SQLiteContactRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.db = connection
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")

    def _build(self, row: sqlite3.Row) -> Contact:
        phones = self.db.execute(
            'SELECT phone_number FROM "Phone_Number" WHERE contact_id = ? ORDER BY id',
            (row["id"],),
        ).fetchall()
        return Contact(
            id=row["id"], user_id=row["user_id"], full_name=row["full_name"],
            email=row["email"] or "", address=row["address"] or "",
            phone_numbers=tuple(p["phone_number"] for p in phones),
        )

    def create(self, contact: Contact) -> Contact:
        try:
            with self.db:
                cur = self.db.execute(
                    'INSERT INTO "Contact" (user_id, full_name, email, address) '
                    'VALUES (?, ?, ?, ?)',
                    (contact.user_id, contact.full_name, contact.email, contact.address),
                )
                ident = cur.lastrowid
                for number in contact.phone_numbers:
                    self.db.execute(
                        'INSERT INTO "Phone_Number" (contact_id, phone_number, label) '
                        'VALUES (?, ?, ?)', (ident, number, "mobile"),
                    )
        except sqlite3.IntegrityError as exc:
            raise ContactValidationError("Database rejected contact or unknown user_id") from exc
        return self.get(contact.user_id, ident)  # type: ignore[return-value]

    def get(self, user_id: int, contact_id: int) -> Contact | None:
        row = self.db.execute(
            'SELECT id, user_id, full_name, email, address FROM "Contact" '
            'WHERE id = ? AND user_id = ?', (contact_id, user_id),
        ).fetchone()
        return self._build(row) if row else None

    def list_by_user(self, user_id: int) -> list[Contact]:
        rows = self.db.execute(
            'SELECT id, user_id, full_name, email, address FROM "Contact" '
            'WHERE user_id = ? ORDER BY full_name COLLATE NOCASE, id', (user_id,),
        ).fetchall()
        return [self._build(row) for row in rows]

    def update(self, contact: Contact) -> Contact:
        with self.db:
            cur = self.db.execute(
                'UPDATE "Contact" SET full_name = ?, email = ?, address = ? '
                'WHERE id = ? AND user_id = ?',
                (contact.full_name, contact.email, contact.address,
                 contact.id, contact.user_id),
            )
            if cur.rowcount != 1:
                raise ContactNotFound("Contact not found")
            self.db.execute('DELETE FROM "Phone_Number" WHERE contact_id = ?',
                            (contact.id,))
            for number in contact.phone_numbers:
                self.db.execute(
                    'INSERT INTO "Phone_Number" (contact_id, phone_number, label) '
                    'VALUES (?, ?, ?)', (contact.id, number, "mobile"),
                )
        return self.get(contact.user_id, contact.id)  # type: ignore[arg-type,return-value]

    def delete(self, user_id: int, contact_id: int) -> bool:
        with self.db:
            cur = self.db.execute(
                'DELETE FROM "Contact" WHERE id = ? AND user_id = ?',
                (contact_id, user_id),
            )
        return cur.rowcount == 1
