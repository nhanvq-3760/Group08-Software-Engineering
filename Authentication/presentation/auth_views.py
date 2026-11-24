
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

from business.auth_service import AuthService, AuthError
from database.connection import get_connection

from contact_management import (
    ContactService,
    SQLiteContactRepository,
    ContactController,
)
from ContactGroups.presentation.contact_group_views import ContactGroupWindow
from presentation.contact_views import ContactWindow
from ContactGroups.contact_groups import (
    SQLiteGroupRepository,
    ContactGroupService,
    ContactGroupController,
)

from admin.admin_gui import open_admin_window

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book Management System")
        self.root.geometry("900x600")

        self.auth = AuthService()

        self.contact_conn = get_connection()
        repository = SQLiteContactRepository(self.contact_conn)
        service = ContactService(repository)
        self.contact_controller = ContactController(service)

        group_repository = SQLiteGroupRepository(self.contact_conn)
        group_service = ContactGroupService(group_repository)
        self.group_controller = ContactGroupController(group_service)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.show_login()

    def on_close(self):
        self.contact_conn.close()
        self.root.destroy()

    def current_user_id(self):
        return self.auth.current_user["user_id"]

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_label_entry(self, parent, label, show=None):
        tk.Label(parent, text=label).pack(
            anchor="w", padx=35, pady=(8, 2)
        )
        entry = tk.Entry(parent, show=show, width=42)
        entry.pack(padx=35)
        return entry

    # AUTHENTICATION

    def show_login(self):
        self.clear()
        self.root.geometry("430x430")

        tk.Label(
            self.root,
            text="Phone Book - Login",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        self.login_entry = self.make_label_entry(
            self.root, "Username or Email"
        )
        self.password_entry = self.make_label_entry(
            self.root, "Password", show="*"
        )

        tk.Button(
            self.root, text="Log In", width=25,
            command=self.do_login
        ).pack(pady=18)

        tk.Button(
            self.root, text="Create an account",
            command=self.show_register
        ).pack()

    def do_login(self):
        try:
            self.auth.login(
                self.login_entry.get(),
                self.password_entry.get()
            )
            self.show_home()
        except AuthError as error:
            messagebox.showerror("Login failed", str(error))

    def show_register(self):
        self.clear()

        tk.Label(
            self.root, text="Create Account",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        self.reg_username = self.make_label_entry(
            self.root, "Username"
        )
        self.reg_email = self.make_label_entry(
            self.root, "Email"
        )
        self.reg_password = self.make_label_entry(
            self.root, "Password", show="*"
        )
        self.reg_confirm = self.make_label_entry(
            self.root, "Confirm password", show="*"
        )

        tk.Button(
            self.root, text="Register", width=25,
            command=self.do_register
        ).pack(pady=15)

        tk.Button(
            self.root, text="Back to login",
            command=self.show_login
        ).pack()

    def do_register(self):
        try:
            self.auth.register(
                self.reg_username.get(),
                self.reg_email.get(),
                self.reg_password.get(),
                self.reg_confirm.get()
            )
            messagebox.showinfo(
                "Success",
                "Account created. You can now log in."
            )
            self.show_login()
        except AuthError as error:
            messagebox.showerror(
                "Registration failed", str(error)
            )

    def show_home(self):
        self.clear()
        self.root.geometry("430x430")

        user = self.auth.current_user

        tk.Label(
            self.root,
            text="Welcome to Phone Book",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text=f"Logged in as: {user['username']}"
        ).pack(pady=5)

        tk.Button(
            self.root, text="Contact Management",
            width=25, command=self.show_contacts
        ).pack(pady=10)

        tk.Button(
            self.root, text="Contact Groups",
            width=25, command=self.show_contact_groups
        ).pack(pady=5)
        if user.get("role") == "admin":
            tk.Button(
                self.root,
                text="Admin Management",
                width=25,
                command=self.show_admin
            ).pack(pady=5)
        tk.Button(
            self.root, text="Update Profile",
            width=25, command=self.show_profile
        ).pack(pady=5)

        tk.Button(
            self.root, text="Log Out",
            width=25, command=self.do_logout
        ).pack(pady=5)
    def show_admin(self):
        user = self.auth.current_user

        if user.get("role") != "admin":
            messagebox.showerror(
                "Access Denied",
                "You do not have permission to access Admin Management."
            )
            return

        open_admin_window(
            self.root,
            user["user_id"]
        )
    # CONTACT MANAGEMENT

    def show_contacts(self):
        ContactWindow(
            self.root,
            self.current_user_id(),
            self.contact_controller,
            self.show_home
        )
    # PROFILE

    def show_profile(self):
        self.clear()
        self.root.geometry("430x430")

        user = self.auth.current_user

        tk.Label(
            self.root, text="Update Profile",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        self.profile_username = self.make_label_entry(
            self.root, "Username"
        )
        self.profile_username.insert(
            0, user["username"]
        )

        self.profile_email = self.make_label_entry(
            self.root, "Email"
        )
        self.profile_email.insert(
            0, user["email"]
        )

        tk.Button(
            self.root, text="Save Changes",
            width=25, command=self.do_update_profile
        ).pack(pady=15)

        tk.Button(
            self.root, text="Cancel",
            command=self.show_home
        ).pack()

    def do_update_profile(self):
        try:
            self.auth.update_profile(
                self.profile_username.get(),
                self.profile_email.get()
            )

            messagebox.showinfo(
                "Success", "Profile updated."
            )

            self.show_home()

        except AuthError as error:
            messagebox.showerror(
                "Update failed", str(error)
            )

    # LOGOUT

    def do_logout(self):
        self.auth.logout()
        self.show_login()






    # CONTACT GROUP MANAGEMENT

    def show_contact_groups(self):
        ContactGroupWindow(
            self.root,
            self.current_user_id(),
            self.group_controller,
            self.contact_controller
        )


