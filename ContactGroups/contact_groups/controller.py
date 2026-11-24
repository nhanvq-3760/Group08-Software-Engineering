"""Controller facade for Member 1 to connect authenticated sessions."""
class ContactGroupController:
    def __init__(self, service): self.service = service
    def create(self, current_user_id, name): return self.service.create(current_user_id, name).__dict__
    def list(self, current_user_id): return [g.__dict__ for g in self.service.list(current_user_id)]
    def view(self, current_user_id, group_id): return self.service.view(current_user_id, group_id).__dict__
    def rename(self, current_user_id, group_id, name): return self.service.rename(current_user_id, group_id, name).__dict__
    def delete(self, current_user_id, group_id): self.service.delete(current_user_id, group_id); return True
    def add_contact(self, current_user_id, group_id, contact_id): self.service.add_contact(current_user_id, group_id, contact_id); return True
    def remove_contact(self, current_user_id, group_id, contact_id): self.service.remove_contact(current_user_id, group_id, contact_id); return True
