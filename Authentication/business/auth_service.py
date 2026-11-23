
import hashlib
import hmac
import os
import re
from data_access.user_repository import UserRepository


class AuthError(Exception):
    pass


class AuthService:
    ITERATIONS = 310_000

    def __init__(self, repository=None):
        self.repository = repository or UserRepository()
        self.current_user = None

    @staticmethod
    def _hash_password(password, salt=None):
        salt = salt or os.urandom(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, AuthService.ITERATIONS
        )
        return salt.hex() + "$" + digest.hex()

    @staticmethod
    def _verify_password(password, stored_hash):
        try:
            salt_hex, digest_hex = stored_hash.split("$", 1)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, AuthService.ITERATIONS
            )
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False

    def register(self, username, email, password, confirm_password):
        username = username.strip()
        email = email.strip().lower()

        if not username or not email or not password or not confirm_password:
            raise AuthError("Please fill in all fields.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise AuthError("Please enter a valid email address.")
        if len(password) < 8:
            raise AuthError("Password must contain at least 8 characters.")
        if password != confirm_password:
            raise AuthError("Passwords do not match.")
        if self.repository.find_by_username_or_email(username, email):
            raise AuthError("Username or email already exists.")

        password_hash = self._hash_password(password)
        return self.repository.create_user(username, email, password_hash)

    def login(self, login, password):
        if not login.strip() or not password:
            raise AuthError("Enter your username/email and password.")

        user = self.repository.find_by_login(login.strip())

        if not user or not self._verify_password(password, user["PasswordHash"]):
            raise AuthError("Invalid username/email or password.")

        if user["is_active"] != 1:
            raise AuthError("Your account has been deactivated. Please contact the administrator.")

        self.current_user = {
            "user_id": user["UserID"],
            "username": user["UserName"],
            "email": user["Email"],
            "role": user["role"],
            "is_active": user["is_active"]
        }

        return self.current_user

    def update_profile(self, username, email):
        if not self.current_user:
            raise AuthError("Please log in first.")

        username = username.strip()
        email = email.strip().lower()

        if not username or not email:
            raise AuthError("Username and email are required.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise AuthError("Please enter a valid email address.")

        existing = self.repository.find_by_username_or_email(username, email)
        if existing and existing["UserID"] != self.current_user["user_id"]:
            raise AuthError("Username or email is already used by another account.")

        self.repository.update_profile(
            self.current_user["user_id"], username, email
        )

        self.current_user["username"] = username
        self.current_user["email"] = email

        return self.current_user

    def logout(self):
        self.current_user = None
