"""Business logic for Admin user-account management."""
from database import get_connection
from security import hash_password

class AdminService:
    def __init__(self, db_path):
        self.db_path = db_path

    def list_users(self):
        with get_connection(self.db_path) as conn:
            rows = conn.execute("""
                SELECT user_id, username, email, role, is_active, created_at
                FROM User ORDER BY user_id
            """).fetchall()
            return [dict(row) for row in rows]

    def create_user(self, username, email, password, role="user"):
        username, email = username.strip(), email.strip().lower()
        if not username or not email or not password:
            raise ValueError("Username, email and password are required")
        if role not in ("user", "admin"):
            raise ValueError("Invalid role")
        with get_connection(self.db_path) as conn:
            conn.execute("""
                INSERT INTO User(username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (username, email, hash_password(password), role))

    def set_user_status(self, user_id, is_active):
        if is_active not in (0, 1):
            raise ValueError("Status must be 0 or 1")
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE User SET is_active=? WHERE user_id=?",
                (is_active, user_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("User not found")

    def change_role(self, user_id, role):
        if role not in ("user", "admin"):
            raise ValueError("Invalid role")
        with get_connection(self.db_path) as conn:
            cursor = conn.execute("UPDATE User SET role=? WHERE user_id=?", (role, user_id))
            if cursor.rowcount == 0:
                raise ValueError("User not found")

    def delete_user(self, user_id, current_admin_id):
        if int(user_id) == int(current_admin_id):
            raise ValueError("Admin cannot delete the currently logged-in account")
        with get_connection(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM User WHERE user_id=?", (user_id,))
            if cursor.rowcount == 0:
                raise ValueError("User not found")
