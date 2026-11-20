import pytest
from business.auth_service import AuthService, AuthError

class FakeUserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def find_by_username_or_email(self, username, email):
        for user in self.users:
            if user["UserName"].lower() == username.lower() or user["Email"].lower() == email.lower():
                return {"UserID": user["UserID"]}
        return None

    def create_user(self, username, email, password_hash):
        user = {
            "UserID": self.next_id, "UserName": username,
            "Email": email, "PasswordHash": password_hash
        }
        self.users.append(user)
        self.next_id += 1
        return user["UserID"]

    def find_by_login(self, login):
        for user in self.users:
            if user["UserName"].lower() == login.lower() or user["Email"].lower() == login.lower():
                return user
        return None

    def update_profile(self, user_id, username, email):
        for user in self.users:
            if user["UserID"] == user_id:
                user["UserName"] = username
                user["Email"] = email

def test_register_and_login():
    service = AuthService(FakeUserRepository())
    service.register("alice", "alice@example.com", "password123", "password123")
    user = service.login("alice", "password123")
    assert user["username"] == "alice"

def test_duplicate_registration():
    service = AuthService(FakeUserRepository())
    service.register("alice", "alice@example.com", "password123", "password123")
    with pytest.raises(AuthError):
        service.register("alice", "other@example.com", "password123", "password123")

def test_wrong_password():
    service = AuthService(FakeUserRepository())
    service.register("alice", "alice@example.com", "password123", "password123")
    with pytest.raises(AuthError):
        service.login("alice", "wrongpassword")

def test_logout():
    service = AuthService(FakeUserRepository())
    service.register("alice", "alice@example.com", "password123", "password123")
    service.login("alice", "password123")
    service.logout()
    assert service.current_user is None
