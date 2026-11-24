
import tkinter as tk
from tkinter import ttk, messagebox


class ContactWindow:
    def __init__(self, root, user_id, contact_controller, show_home):
        self.root = root
        self.user_id = user_id
        self.contact_controller = contact_controller
        self.show_home = show_home

        self.clear_root()
        self.show_contacts()

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

    def show_contacts(self):
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
            width=10, command=self.go_home
        ).pack(side="left", padx=5)

        self.refresh_contacts()

    def refresh_contacts(self):
        try:
            contacts = self.contact_controller.list(self.user_id)
            self.display_contacts(contacts)
        except Exception as error:
            messagebox.showerror("Error", str(error))

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
                self.user_id, query
            )
            self.display_contacts(contacts)
        except Exception as error:
            messagebox.showerror("Search failed", str(error))

    def select_contact(self, event=None):
        selected = self.contact_tree.selection()

        if not selected:
            return

        contact_id = int(selected[0])

        try:
            contact = self.contact_controller.view(
                self.user_id, contact_id
            )

            self.clear_form()

            self.contact_name.insert(0, contact["full_name"])
            self.contact_email.insert(0, contact["email"])
            self.contact_phone.insert(
                0, ", ".join(contact["phone_numbers"])
            )
            self.contact_address.insert(0, contact["address"])

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def add_contact(self):
        try:
            self.contact_controller.add(
                self.user_id, self.get_contact_payload()
            )

            messagebox.showinfo(
                "Success", "Contact added successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror("Add failed", str(error))

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
                self.user_id,
                contact_id,
                self.get_contact_payload()
            )

            messagebox.showinfo(
                "Success", "Contact updated successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror("Update failed", str(error))

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
                self.user_id, contact_id
            )

            messagebox.showinfo(
                "Success", "Contact deleted successfully."
            )

            self.clear_form()
            self.refresh_contacts()

        except Exception as error:
            messagebox.showerror("Delete failed", str(error))

    def clear_form(self):
        self.contact_name.delete(0, tk.END)
        self.contact_email.delete(0, tk.END)
        self.contact_phone.delete(0, tk.END)
        self.contact_address.delete(0, tk.END)

    def go_home(self):
        self.clear_root()
        self.show_home()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

