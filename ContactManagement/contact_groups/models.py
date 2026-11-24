"""Domain models and exceptions for Contact Group Management."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ContactGroup:
    id: int
    user_id: int
    group_name: str
    contacts: tuple[dict, ...] = ()

class GroupValidationError(ValueError):
    pass

class GroupNotFound(LookupError):
    """Group not found or not owned by the current user."""

class ContactNotFound(LookupError):
    """Contact not found or not owned by the current user."""
