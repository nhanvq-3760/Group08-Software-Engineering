
import sys
from pathlib import Path

AUTH_PATH = Path(__file__).resolve().parent.parent / "Authentication"

if str(AUTH_PATH) not in sys.path:
    sys.path.insert(0, str(AUTH_PATH))

from data_access.user_repository import UserRepository


class AdminService:
    def __init__(self, db_path=None):
        self.repository = UserRepository()

    def list_users(self):
        return self.repository.list_users()

    def set_user_status(self, user_id, is_active):
        self.repository.set_user_status(user_id, is_active)

    def change_role(self, user_id, role):
        self.repository.change_role(user_id, role)

    def delete_user(self, user_id, current_admin_id):
        if int(user_id) == int(current_admin_id):
            raise ValueError(
                "Admin cannot delete the currently logged-in account."
            )

        self.repository.delete_user(user_id)
