from __future__ import annotations
"""Framework-neutral controller for later integration by Member 1.

IMPORTANT: user_id MUST come from a verified login/session token.
Never accept user_id submitted by the client as proof of identity.
"""
from .service import ContactService


class ContactController:
    def __init__(self, service: ContactService):
        self.service = service

    def add(self, authenticated_user_id: int, payload: dict) -> dict:
        c = self.service.add_contact(
            authenticated_user_id, payload["full_name"],
            email=payload.get("email", ""), address=payload.get("address", ""),
            phone_numbers=payload.get("phone_numbers", []),
        )
        return c.to_dict()

    def list(self, authenticated_user_id: int) -> list[dict]:
        return [c.to_dict() for c in self.service.view_contacts(authenticated_user_id)]

    def search(self, authenticated_user_id: int, query: str) -> list[dict]:
        return [c.to_dict() for c in self.service.search_contacts(authenticated_user_id, query)]

    def view(self, authenticated_user_id: int, contact_id: int) -> dict:
        return self.service.view_contact(authenticated_user_id, contact_id).to_dict()

    def edit(self, authenticated_user_id: int, contact_id: int, payload: dict) -> dict:
        fields = ("full_name", "email", "address", "phone_numbers")
        return self.service.update_contact(
            authenticated_user_id, contact_id,
            **{key: payload[key] for key in fields if key in payload},
        ).to_dict()

    def remove(self, authenticated_user_id: int, contact_id: int) -> dict:
        self.service.delete_contact(authenticated_user_id, contact_id)
        return {"deleted": True, "id": contact_id}
