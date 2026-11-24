# Member 3 Integration Contract

Member 3 exposes the UI-independent `ContactGroupService` and `ContactGroupController`.

## Controller calls
```python
controller.create(current_user_id, name)
controller.list(current_user_id)
controller.view(current_user_id, group_id)
controller.rename(current_user_id, group_id, name)
controller.delete(current_user_id, group_id)
controller.add_contact(current_user_id, group_id, contact_id)
controller.remove_contact(current_user_id, group_id, contact_id)
```

`current_user_id` must be taken from Member 1's authenticated session, not from a user-controlled form/request. Member 3 validates group ownership and contact ownership before membership changes.

## Database assumptions (confirm with Member 4)
- `Contact_Group`: `id`, `user_id`, `group_name`; unique `(user_id, group_name)`.
- `Contact_Group_Member`: `group_id`, `contact_id`; composite PK; foreign keys to `Contact_Group.id` and `Contact.id`, preferably `ON DELETE CASCADE`.
- Contact table has `id`, `user_id`, `full_name`, `email`, `address`.

Demo-only schema is `database/schema_member3_demo.sql`. Do not run it on the production database. Align actual column names/migrations with Member 4 before integration. Existing Member 2 source has not been modified by Member 3.
