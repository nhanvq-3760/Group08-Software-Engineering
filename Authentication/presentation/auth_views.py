
import tkinter as tk
from tkinter import messagebox, ttk

from business.auth_service import AuthService, AuthError
from database.connection import get_connection

from contact_management import (
    ContactService,
    SQLiteContactRepository,
    ContactController,
)


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
            self.root, text="Update Profile",
            width=25, command=self.show_profile
        ).pack(pady=5)

        tk.Button(
            self.root, text="Log Out",
            width=25, command=self.do_logout
        ).pack(pady=5)

    # CONTACT MANAGEMENT

    def show_contacts(self):
        self.clear()
        self.root.geometry("1000x650")

        tk.Label(
            self.root,
            text="Contact Management",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(search_frame, text="Search:").pack(side="left")

        self.search_entry = tk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=8)

        tk.Button(
            search_frame, text="Search",
            command=self.search_contacts
        ).pack(side="left", padx=3)

        tk.Button(
            search_frame, text="Show All",
            command=self.refresh_contacts
        ).pack(side="left", padx=3)

        columns = (
            "id", "full_name", "email",
            "phone_numbers", "address"
        )

        self.contact_tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "id": "ID",
            "full_name": "Full Name",
            "email": "Email",
            "phone_numbers": "Phone Numbers",
            "address": "Address"
        }

        widths = {
            "id": 50,
            "full_name": 180,
            "email": 180,
            "phone_numbers": 180,
            "address": 250
        }

        for column in columns:
            self.contact_tree.heading(
                column, text=headings[column]
            )
            self.contact_tree.column(
                column, width=widths[column]
            )

        self.contact_tree.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        self.contact_tree.bind(
            "<<TreeviewSelect>>",
            self.select_contact
        )

        form = tk.LabelFrame(
            self.root, text="Contact Information"
        )
        form.pack(fill="x", padx=20, pady=5)

        self.contact_name = self.make_form_entry(
            form, "Full Name", 0
        )
        self.contact_email = self.make_form_entry(
            form, "Email", 1
        )
        self.contact_phone = self.make_form_entry(
            form, "Phone Numbers (comma separated)", 2
        )
        self.contact_address = self.make_form_entry(
            form, "Address", 3
        )

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=12)

        tk.Button(
            button_frame, text="Add Contact",
            width=15, command=self.add_contact
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Update Contact",
            width=15, command=self.update_contact
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Delete Contact",
            width=15, command=self.delete_contact
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Clear Form",
            width=12, command=self.clear_form
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Back",
            width=10, command=self.show_home
        ).pack(side="left", padx=5)

        self.refresh_contacts()

    def make_form_entry(self, parent, label, row):
        tk.Label(
            parent, text=label
        ).grid(row=row, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(parent, width=65)
        entry.grid(row=row, column=1, padx=10, pady=5)

        return entry

    def get_contact_payload(self):
        phones = [
            phone.strip()
            for phone in self.contact_phone.get().split(",")
            if phone.strip()
        ]

        return {
            "full_name": self.contact_name.get(),
            "email": self.contact_email.get(),
            "address": self.contact_address.get(),
            "phone_numbers": phones
        }

    def refresh_contacts(self):
        try:
            contacts = self.contact_controller.list(
                self.current_user_id()
            )
            self.display_contacts(contacts)
        except Exception as error:
            messagebox.showerror(
                "Error", str(error)
            )

    def display_contacts(self, contacts):
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)

        for contact in contacts:
            self.contact_tree.insert(
                "",
                "end",
                iid=str(contact["id"]),
                values=(
                    contact["id"],
                    contact["full_name"],
                    contact["email"],
                    ", ".join(contact["phone_numbers"]),
                    contact["address"]
                )
            )

    def search_contacts(self):
        query = self.search_entry.get().strip()

        if not query:
            self.refresh_contacts()
            return

        try:
            contacts = self.contact_controller.search(
                self.current_user_id(), query
            )
            self.display_contacts(contacts)
        except Exception as error:
            messagebox.showerror(
                "Search failed", str(error)
            )

    def select_contact(self, event=None):
        selected = self.contact_tree.selection()

        if not selected:
            return

        contact_id = int(selected[0])

        try:
            contact = self.contact_controller.view(
                self.current_user_id(), contact_id
            )

            self.clear_form()

            self.contact_name.insert(
                0, contact["full_name"]
            )
            self.contact_email.insert(
                0, contact["email"]
            )
            self.contact_phone.insert(
                0, ", ".join(contact["phone_numbers"])
            )
            self.contact_address.insert(
                0, contact["address"]
            )

        except Exception as error:
            messagebox.showerror(
                "Error", str(error)
            )

    def add_contact(self):
        try:
            self.contact_controller.add(
                self.current_user_id(),
                self.get_contact_payload()
            )

            messagebox.showinfo(
                "Success", "Contact added successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror(
                "Add failed", str(error)
            )

    def update_contact(self):
        selected = self.contact_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a contact first."
            )
            return

        contact_id = int(selected[0])

        try:
            self.contact_controller.edit(
                self.current_user_id(),
                contact_id,
                self.get_contact_payload()
            )

            messagebox.showinfo(
                "Success", "Contact updated successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror(
                "Update failed", str(error)
            )

    def delete_contact(self):
        selected = self.contact_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a contact first."
            )
            return

        contact_id = int(selected[0])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this contact?"
        )

        if not confirm:
            return

        try:
            self.contact_controller.remove(
                self.current_user_id(), contact_id
            )

            messagebox.showinfo(
                "Success", "Contact deleted successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror(
                "Delete failed", str(error)
            )

    def clear_form(self):
        self.contact_name.delete(0, tk.END)
        self.contact_email.delete(0, tk.END)
        self.contact_phone.delete(0, tk.END)
        self.contact_address.delete(0, tk.END)

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
