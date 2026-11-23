
from database.connection import get_connection


class UserRepository:
    def create_user(self, username, email, password_hash):
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO User (UserName, Email, PasswordHash)
                VALUES (?, ?, ?)
                """,
                (username, email, password_hash)
            )
            return cursor.lastrowid

    def find_by_login(self, login):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT UserID, UserName, Email, PasswordHash, role, is_active
                FROM User
                WHERE lower(UserName) = lower(?)
                   OR lower(Email) = lower(?)
                """,
                (login, login)
            ).fetchone()

    def find_by_username_or_email(self, username, email):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT UserID
                FROM User
                WHERE lower(UserName) = lower(?)
                   OR lower(Email) = lower(?)
                """,
                (username, email)
            ).fetchone()

    def update_profile(self, user_id, username, email):
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE User
                SET UserName = ?, Email = ?
                WHERE UserID = ?
                """,
                (username, email, user_id)
            )

    def find_by_id(self, user_id):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT UserID, UserName, Email, role, is_active
                FROM User
                WHERE UserID = ?
                """,
                (user_id,)
            ).fetchone()

    def list_users(self):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT UserID, UserName, Email, role, is_active, CreatedAt
                FROM User
                ORDER BY UserID
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def set_user_status(self, user_id, is_active):
        if is_active not in (0, 1):
            raise ValueError("Status must be 0 or 1.")

        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE User SET is_active = ? WHERE UserID = ?",
                (is_active, user_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("User not found.")

    def change_role(self, user_id, role):
        if role not in ("user", "admin"):
            raise ValueError("Invalid role.")

        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE User SET role = ? WHERE UserID = ?",
                (role, user_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("User not found.")

    def delete_user(self, user_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM User WHERE UserID = ?",
                (user_id,)
            )
            if cursor.rowcount == 0:
                raise ValueError("User not found.")
