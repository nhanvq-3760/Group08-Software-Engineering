"""Domain types and errors: no database or UI dependencies."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Contact:
    id: int | None
    user_id: int
    full_name: str
    email: str = ""
    address: str = ""
    phone_numbers: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone_numbers": list(self.phone_numbers),
        }


class ContactValidationError(ValueError):
    """Invalid Contact Management input."""


class ContactNotFound(LookupError):
    """Not found OR not owned by the authenticated user (avoid enumeration)."""
