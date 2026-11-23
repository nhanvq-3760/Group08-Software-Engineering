"""Basic Tkinter Admin screen. Call open_admin_window(db_path, admin_id)."""
import tkinter as tk
from tkinter import ttk, messagebox
from admin_service import AdminService

def open_admin_window(db_path, admin_id):
    service = AdminService(db_path)
    window = tk.Tk()
    window.title("Phone Book - Admin Management")
    window.geometry("850x460")

    columns = ("user_id", "username", "email", "role", "is_active", "created_at")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=14)
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=130 if col != "created_at" else 170)
    tree.pack(fill="both", expand=True, padx=12, pady=12)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        for user in service.list_users():
            tree.insert("", "end", values=tuple(user[c] for c in columns))

    def selected_id():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select user", "Please select a user first.")
            return None
        return int(tree.item(selected[0], "values")[0])

    def set_status(status):
        uid = selected_id()
        if uid is None: return
        try:
            service.set_user_status(uid, status)
            refresh()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_selected():
        uid = selected_id()
        if uid is None: return
        if not messagebox.askyesno("Confirm", "Delete this user and related records?"):
            return
        try:
            service.delete_user(uid, admin_id)
            refresh()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    actions = ttk.Frame(window)
    actions.pack(pady=(0, 12))
    ttk.Button(actions, text="Refresh", command=refresh).pack(side="left", padx=5)
    ttk.Button(actions, text="Deactivate", command=lambda: set_status(0)).pack(side="left", padx=5)
    ttk.Button(actions, text="Activate", command=lambda: set_status(1)).pack(side="left", padx=5)
    ttk.Button(actions, text="Delete User", command=delete_selected).pack(side="left", padx=5)
    refresh()
    window.mainloop()

if __name__ == "__main__":
    from pathlib import Path
    from database import initialize_database, DB_PATH
    initialize_database()
    print("Create/login an admin account through your group's authentication module,")
    print("then call open_admin_window(DB_PATH, admin_id).")
