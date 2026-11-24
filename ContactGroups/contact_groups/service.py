"""Use-case layer for Group Management. UI-independent and ownership-safe."""
from .models import GroupValidationError

class ContactGroupService:
    def __init__(self, repository): self.repo = repository

    @staticmethod
    def _validate_user(user_id):
        if not isinstance(user_id, int) or user_id <= 0: raise GroupValidationError("Invalid user ID")
    @staticmethod
    def _validate_group_id(group_id):
        if not isinstance(group_id, int) or group_id <= 0: raise GroupValidationError("Invalid group ID")
    @staticmethod
    def _name(name):
        if not isinstance(name, str): raise GroupValidationError("Group name must be text")
        name = name.strip()
        if not name: raise GroupValidationError("Group name cannot be blank")
        if len(name) > 50: raise GroupValidationError("Group name must be at most 50 characters")
        return name

    def create(self, user_id, name):
        self._validate_user(user_id); return self.repo.create_group(user_id, self._name(name))
    def list(self, user_id):
        self._validate_user(user_id); return self.repo.list_groups(user_id)
    def view(self, user_id, group_id):
        self._validate_user(user_id); self._validate_group_id(group_id)
        group = self.repo.get_group(user_id, group_id)
        if group is None:
            from .models import GroupNotFound
            raise GroupNotFound("Group not found")
        return group
    def rename(self, user_id, group_id, name):
        self._validate_user(user_id); self._validate_group_id(group_id)
        return self.repo.rename_group(user_id, group_id, self._name(name))
    def delete(self, user_id, group_id):
        self._validate_user(user_id); self._validate_group_id(group_id)
        if not self.repo.delete_group(user_id, group_id):
            from .models import GroupNotFound
            raise GroupNotFound("Group not found")
    def add_contact(self, user_id, group_id, contact_id):
        self._validate_user(user_id); self._validate_group_id(group_id); self._validate_group_id(contact_id)
        self.repo.add_contact(user_id, group_id, contact_id)
    def remove_contact(self, user_id, group_id, contact_id):
        self._validate_user(user_id); self._validate_group_id(group_id); self._validate_group_id(contact_id)
        if not self.repo.remove_contact(user_id, group_id, contact_id):
            from .models import GroupNotFound
            raise GroupNotFound("Membership not found")
