import sqlite3
from database import initialize_database, get_connection, check_integrity

def test_all_five_tables_created(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    with get_connection(db) as conn:
        names = {r["name"] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert {"User", "Contact", "Phone_Number", "Contact_Group",
            "Contact_Group_Member"}.issubset(names)

def test_foreign_key_prevents_orphan_contact(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    with get_connection(db) as conn:
        try:
            conn.execute("INSERT INTO Contact(user_id, full_name) VALUES (999, 'Orphan')")
            assert False, "Expected foreign-key failure"
        except sqlite3.IntegrityError:
            pass

def test_cascade_delete_removes_user_contacts(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    with get_connection(db) as conn:
        conn.execute("INSERT INTO User(username,email,password_hash) VALUES ('a','a@x.com','x')")
        uid = conn.execute("SELECT user_id FROM User").fetchone()[0]
        conn.execute("INSERT INTO Contact(user_id,full_name) VALUES (?, 'Test')", (uid,))
        conn.execute("DELETE FROM User WHERE user_id=?", (uid,))
        assert conn.execute("SELECT COUNT(*) FROM Contact").fetchone()[0] == 0

def test_integrity_check_is_ok(tmp_path):
    db = tmp_path / "test.db"
    initialize_database(db)
    result = check_integrity(db)
    assert result["integrity_check"] == "ok"
    assert result["foreign_key_errors"] == []
