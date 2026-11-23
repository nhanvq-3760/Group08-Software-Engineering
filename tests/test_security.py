import pytest
from security import hash_password, verify_password

def test_password_hash_verifies():
    encoded = hash_password("StrongPass123!")
    assert encoded != "StrongPass123!"
    assert verify_password("StrongPass123!", encoded)

def test_wrong_password_fails():
    encoded = hash_password("StrongPass123!")
    assert not verify_password("wrong", encoded)

def test_empty_password_rejected():
    with pytest.raises(ValueError):
        hash_password("")
