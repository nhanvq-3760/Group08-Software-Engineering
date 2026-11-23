import pytest
from database import initialize_database, get_connection
from admin_service import AdminService

def setup_db(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    with get_connection(db) as conn:
        conn.execute(
            "INSERT INTO User(username,email,password_hash,role) VALUES ('admin','admin@test.com','x','admin')"
        )
        conn.execute(
            "INSERT INTO User(username,email,password_hash) VALUES ('user','user@test.com','x')"
        )
    return db

def test_admin_lists_users(tmp_path):
    db = setup_db(tmp_path)
    assert len(AdminService(db).list_users()) == 2

def test_admin_deactivates_user(tmp_path):
    db = setup_db(tmp_path)
    service = AdminService(db)
    user_id = service.list_users()[1]["user_id"]
    service.set_user_status(user_id, 0)
    assert service.list_users()[1]["is_active"] == 0

def test_admin_cannot_delete_self(tmp_path):
    db = setup_db(tmp_path)
    service = AdminService(db)
    admin_id = service.list_users()[0]["user_id"]
    with pytest.raises(ValueError):
        service.delete_user(admin_id, admin_id)

def test_duplicate_email_is_rejected(tmp_path):
    db = setup_db(tmp_path)
    with pytest.raises(Exception):
        AdminService(db).create_user("another", "user@test.com", "pass")
