
import tkinter as tk
from tkinter import ttk, messagebox

from admin.admin_service import AdminService


def open_admin_window(parent, admin_id):
    service = AdminService()

    window = tk.Toplevel(parent)
    window.title("Phone Book - Admin Management")
    window.geometry("950x500")
    window.transient(parent)

    columns = (
        "UserID",
        "UserName",
        "Email",
        "role",
        "is_active",
        "CreatedAt"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=15
    )

    headings = {
        "UserID": "User ID",
        "UserName": "Username",
        "Email": "Email",
        "role": "Role",
        "is_active": "Status",
        "CreatedAt": "Created At"
    }

    widths = {
        "UserID": 70,
        "UserName": 160,
        "Email": 210,
        "role": 90,
        "is_active": 80,
        "CreatedAt": 180
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=widths[column])

    tree.pack(fill="both", expand=True, padx=12, pady=12)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)

        for user in service.list_users():
            tree.insert(
                "",
                "end",
                values=tuple(user[column] for column in columns)
            )

    def selected_user():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select User",
                "Please select a user first.",
                parent=window
            )
            return None

        values = tree.item(selected[0], "values")

        return {
            "id": int(values[0]),
            "username": values[1],
            "role": values[3],
            "is_active": int(values[4])
        }

    def set_status(status):
        user = selected_user()

        if user is None:
            return

        if user["id"] == admin_id and status == 0:
            messagebox.showwarning(
                "Warning",
                "You cannot deactivate your own account.",
                parent=window
            )
            return

        try:
            service.set_user_status(user["id"], status)
            refresh()

            messagebox.showinfo(
                "Success",
                "Account status updated.",
                parent=window
            )

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=window)

    def change_role(role):
        user = selected_user()

        if user is None:
            return

        if user["id"] == admin_id:
            messagebox.showwarning(
                "Warning",
                "You cannot change your own role.",
                parent=window
            )
            return

        try:
            service.change_role(user["id"], role)
            refresh()

            messagebox.showinfo(
                "Success",
                "User role updated.",
                parent=window
            )

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=window)

    def delete_selected():
        user = selected_user()

        if user is None:
            return

        if user["id"] == admin_id:
            messagebox.showwarning(
                "Warning",
                "You cannot delete your own account.",
                parent=window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this user and all related records?",
            parent=window
        )

        if not confirm:
            return

        try:
            service.delete_user(user["id"], admin_id)
            refresh()

            messagebox.showinfo(
                "Success",
                "User deleted successfully.",
                parent=window
            )

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=window)

    actions = ttk.Frame(window)
    actions.pack(pady=(0, 12))

    ttk.Button(
        actions, text="Refresh", command=refresh
    ).pack(side="left", padx=5)

    ttk.Button(
        actions, text="Activate",
        command=lambda: set_status(1)
    ).pack(side="left", padx=5)

    ttk.Button(
        actions, text="Deactivate",
        command=lambda: set_status(0)
    ).pack(side="left", padx=5)

    ttk.Button(
        actions, text="Set as Admin",
        command=lambda: change_role("admin")
    ).pack(side="left", padx=5)

    ttk.Button(
        actions, text="Set as User",
        command=lambda: change_role("user")
    ).pack(side="left", padx=5)

    ttk.Button(
        actions, text="Delete User",
        command=delete_selected
    ).pack(side="left", padx=5)

    refresh()
