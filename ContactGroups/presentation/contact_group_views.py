import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ContactGroupWindow:
    def __init__(self, root, user_id, group_controller, contact_controller):
        self.user_id = user_id
        self.groups = group_controller
        self.contacts = contact_controller

        self.window = tk.Toplevel(root)
        self.window.title("Contact Group Management")
        self.window.geometry("1050x600")
        self.window.transient(root)

        self.selected_group_id = None
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        tk.Label(
            self.window,
            text="Contact Group Management",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        main = tk.Frame(self.window)
        main.pack(fill="both", expand=True, padx=15, pady=10)

        self.group_tree = self._create_tree(
            main, "Groups",
            ("id", "name"),
            ("ID", "Group Name"),
            (45, 160)
        )

        self.contact_tree = self._create_tree(
            main, "All Contacts",
            ("id", "name", "email"),
            ("ID", "Name", "Email"),
            (40, 120, 130)
        )

        self.member_tree = self._create_tree(
            main, "Group Members",
            ("id", "name", "email"),
            ("ID", "Name", "Email"),
            (40, 120, 130)
        )

        self._button(self.group_tree.master, "Create Group", self.create_group)
        self._button(self.group_tree.master, "Rename Group", self.rename_group)
        self._button(self.group_tree.master, "Delete Group", self.delete_group)

        self._button(
            self.contact_tree.master,
            "Add to Selected Group",
            self.add_contact
        )

        self._button(
            self.member_tree.master,
            "Remove from Group",
            self.remove_contact
        )

        self.group_tree.bind("<<TreeviewSelect>>", self.load_members)

        tk.Button(
            self.window, text="Refresh",
            command=self.refresh
        ).pack(pady=5)

        tk.Button(
            self.window, text="Close",
            command=self.window.destroy
        ).pack(pady=5)

    def _create_tree(self, parent, title, columns, headings, widths):
        frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)
        frame.pack(side="left", fill="both", expand=True, padx=5)

        tree = ttk.Treeview(
            frame, columns=columns,
            show="headings", height=18
        )

        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            tree.column(
                column, width=width,
                anchor="center" if column == "id" else "w"
            )

        tree.pack(fill="both", expand=True)
        return tree

    def _button(self, parent, text, command):
        tk.Button(
            parent, text=text,
            command=command
        ).pack(fill="x", pady=3)

    def _selected_id(self, tree):
        selection = tree.selection()
        return int(selection[0]) if selection else None

    def _show_error(self, title, error):
        messagebox.showerror(title, str(error), parent=self.window)

    def refresh(self):
        try:
            self.group_tree.delete(*self.group_tree.get_children())
            self.contact_tree.delete(*self.contact_tree.get_children())

            for group in self.groups.list(self.user_id):
                self.group_tree.insert(
                    "", "end",
                    iid=str(group["id"]),
                    values=(group["id"], group["group_name"])
                )

            for contact in self.contacts.list(self.user_id):
                self.contact_tree.insert(
                    "", "end",
                    iid=str(contact["id"]),
                    values=(
                        contact["id"],
                        contact["full_name"],
                        contact["email"]
                    )
                )

            if (
                self.selected_group_id is not None
                and self.group_tree.exists(str(self.selected_group_id))
            ):
                self.group_tree.selection_set(str(self.selected_group_id))
                self.load_members()
            else:
                self.selected_group_id = None
                self.member_tree.delete(*self.member_tree.get_children())

        except Exception as error:
            self._show_error("Loading Failed", error)

    def load_members(self, event=None):
        group_id = self._selected_id(self.group_tree)
        self.selected_group_id = group_id
        self.member_tree.delete(*self.member_tree.get_children())

        if group_id is None:
            return

        try:
            group = self.groups.view(self.user_id, group_id)

            for contact in group.get("contacts", ()):
                self.member_tree.insert(
                    "", "end",
                    iid=str(contact["id"]),
                    values=(
                        contact["id"],
                        contact["full_name"],
                        contact.get("email", "")
                    )
                )
        except Exception as error:
            self._show_error("Loading Members Failed", error)

    def create_group(self):
        name = simpledialog.askstring(
            "Create Group", "Enter group name:",
            parent=self.window
        )
        if name is None:
            return

        try:
            group = self.groups.create(self.user_id, name)
            self.selected_group_id = group["id"]
            self.refresh()
            messagebox.showinfo(
                "Success", "Group created successfully.",
                parent=self.window
            )
        except Exception as error:
            self._show_error("Create Group Failed", error)

    def rename_group(self):
        group_id = self.selected_group_id
        if group_id is None:
            messagebox.showwarning(
                "Warning", "Please select a group.",
                parent=self.window
            )
            return

        current_name = self.group_tree.item(
            str(group_id), "values"
        )[1]

        name = simpledialog.askstring(
            "Rename Group", "Enter new group name:",
            initialvalue=current_name,
            parent=self.window
        )
        if name is None:
            return

        try:
            self.groups.rename(self.user_id, group_id, name)
            self.refresh()
            messagebox.showinfo(
                "Success", "Group renamed successfully.",
                parent=self.window
            )
        except Exception as error:
            self._show_error("Rename Failed", error)

    def delete_group(self):
        group_id = self.selected_group_id
        if group_id is None:
            messagebox.showwarning(
                "Warning", "Please select a group.",
                parent=self.window
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Delete this group? Contacts will not be deleted.",
            parent=self.window
        ):
            return

        try:
            self.groups.delete(self.user_id, group_id)
            self.selected_group_id = None
            self.refresh()
            messagebox.showinfo(
                "Success", "Group deleted successfully.",
                parent=self.window
            )
        except Exception as error:
            self._show_error("Delete Failed", error)

    def add_contact(self):
        group_id = self.selected_group_id
        contact_id = self._selected_id(self.contact_tree)

        if group_id is None or contact_id is None:
            messagebox.showwarning(
                "Warning", "Please select a group and a contact.",
                parent=self.window
            )
            return

        try:
            self.groups.add_contact(self.user_id, group_id, contact_id)
            self.load_members()
            messagebox.showinfo(
                "Success", "Contact added to group.",
                parent=self.window
            )
        except Exception as error:
            self._show_error("Add Contact Failed", error)

    def remove_contact(self):
        group_id = self.selected_group_id
        contact_id = self._selected_id(self.member_tree)

        if group_id is None or contact_id is None:
            messagebox.showwarning(
                "Warning", "Please select a group and a member.",
                parent=self.window
            )
            return

        try:
            self.groups.remove_contact(self.user_id, group_id, contact_id)
            self.load_members()
            messagebox.showinfo(
                "Success", "Contact removed from group.",
                parent=self.window
            )
        except Exception as error:
            self._show_error("Remove Contact Failed", error)
