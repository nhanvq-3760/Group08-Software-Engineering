"""Business layer for Member 2: add, view, search, update and delete contacts."""
import re
from dataclasses import replace
from collections.abc import Sequence
from .contracts import ContactRepository
from .models import Contact, ContactNotFound, ContactValidationError

_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_PHONE_RE = re.compile(r"^\+?[0-9 ()\-.]+$")


def _validate_user_id(user_id: int) -> None:
    if type(user_id) is not int or user_id <= 0:
        raise ContactValidationError("user_id must be a positive integer")


def _validate_contact_id(contact_id: int) -> None:
    if type(contact_id) is not int or contact_id <= 0:
        raise ContactValidationError("contact_id must be a positive integer")


def _name(value: str) -> str:
    if not isinstance(value, str):
        raise ContactValidationError("full_name must be text")
    v = " ".join(value.strip().split())
    if not v or len(v) > 120:
        raise ContactValidationError("full_name must contain 1-120 characters")
    return v


def _email(value: str) -> str:
    if not isinstance(value, str):
        raise ContactValidationError("email must be text")
    v = value.strip()
    if len(v) > 254 or (v and not _EMAIL_RE.fullmatch(v)):
        raise ContactValidationError("invalid email")
    return v


def _address(value: str) -> str:
    if not isinstance(value, str):
        raise ContactValidationError("address must be text")
    v = value.strip()
    if len(v) > 300:
        raise ContactValidationError("address must be at most 300 characters")
    return v


def _phones(value: Sequence[str]) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ContactValidationError("phone_numbers must be a list of strings")
    if len(value) > 10:
        raise ContactValidationError("at most 10 phone numbers per contact")
    numbers = []
    for raw in value:
        if not isinstance(raw, str):
            raise ContactValidationError("phone number must be text")
        num = raw.strip()
        digits = re.sub(r"\D", "", num)
        if not _PHONE_RE.fullmatch(num) or len(digits) < 7 or len(digits) > 15:
            raise ContactValidationError("phone number must have 7-15 digits")
        numbers.append(num)
    if len(numbers) != len(set(numbers)):
        raise ContactValidationError("duplicate phone number in one contact")
    return tuple(numbers)


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def add_contact(self, user_id: int, full_name: str, *, email: str = "",
                    address: str = "", phone_numbers: Sequence[str] = ()) -> Contact:
        _validate_user_id(user_id)
        return self.repository.create(Contact(
            id=None, user_id=user_id, full_name=_name(full_name),
            email=_email(email), address=_address(address),
            phone_numbers=_phones(phone_numbers),
        ))

    def view_contacts(self, user_id: int) -> list[Contact]:
        _validate_user_id(user_id)
        return self.repository.list_by_user(user_id)

    def view_contact(self, user_id: int, contact_id: int) -> Contact:
        _validate_user_id(user_id)
        _validate_contact_id(contact_id)
        item = self.repository.get(user_id, contact_id)
        if item is None:
            raise ContactNotFound("Contact not found")
        return item

    def search_contacts(self, user_id: int, query: str) -> list[Contact]:
        _validate_user_id(user_id)
        if not isinstance(query, str):
            raise ContactValidationError("query must be text")
        needle = query.strip().casefold()
        if not needle:
            return self.view_contacts(user_id)
        # Python casefold supports accented Vietnamese characters more reliably
        # than SQLite's default ASCII-focused LIKE/NOCASE.
        return [c for c in self.repository.list_by_user(user_id)
                if any(needle in item.casefold()
                       for item in (c.full_name, c.email, c.address, *c.phone_numbers))]

    def update_contact(self, user_id: int, contact_id: int, *,
                       full_name: str | None = None,
                       email: str | None = None,
                       address: str | None = None,
                       phone_numbers: Sequence[str] | None = None) -> Contact:
        old = self.view_contact(user_id, contact_id)
        new = replace(old,
            full_name=old.full_name if full_name is None else _name(full_name),
            email=old.email if email is None else _email(email),
            address=old.address if address is None else _address(address),
            phone_numbers=old.phone_numbers if phone_numbers is None else _phones(phone_numbers),
        )
        return self.repository.update(new)

    def delete_contact(self, user_id: int, contact_id: int) -> None:
        self.view_contact(user_id, contact_id)  # enforce ownership
        if not self.repository.delete(user_id, contact_id):
            raise ContactNotFound("Contact not found")
