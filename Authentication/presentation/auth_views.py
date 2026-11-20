import tkinter as tk
from tkinter import messagebox
from business.auth_service import AuthService, AuthError

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book Management System")
        self.root.geometry("430x430")
        self.auth = AuthService()
        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_label_entry(self, parent, label, show=None):
        tk.Label(parent, text=label).pack(anchor="w", padx=35, pady=(8, 2))
        entry = tk.Entry(parent, show=show, width=42)
        entry.pack(padx=35)
        return entry

    def show_login(self):
        self.clear()
        tk.Label(self.root, text="Phone Book - Login",
                 font=("Arial", 18, "bold")).pack(pady=20)
        self.login_entry = self.make_label_entry(self.root, "Username or Email")
        self.password_entry = self.make_label_entry(self.root, "Password", show="*")
        tk.Button(self.root, text="Log In", width=25,
                  command=self.do_login).pack(pady=18)
        tk.Button(self.root, text="Create an account",
                  command=self.show_register).pack()

    def do_login(self):
        try:
            user = self.auth.login(
                self.login_entry.get(), self.password_entry.get()
            )
            self.show_home()
        except AuthError as error:
            messagebox.showerror("Login failed", str(error))

    def show_register(self):
        self.clear()
        tk.Label(self.root, text="Create Account",
                 font=("Arial", 18, "bold")).pack(pady=15)
        self.reg_username = self.make_label_entry(self.root, "Username")
        self.reg_email = self.make_label_entry(self.root, "Email")
        self.reg_password = self.make_label_entry(self.root, "Password", show="*")
        self.reg_confirm = self.make_label_entry(self.root, "Confirm password", show="*")
        tk.Button(self.root, text="Register", width=25,
                  command=self.do_register).pack(pady=15)
        tk.Button(self.root, text="Back to login",
                  command=self.show_login).pack()

    def do_register(self):
        try:
            self.auth.register(
                self.reg_username.get(), self.reg_email.get(),
                self.reg_password.get(), self.reg_confirm.get()
            )
            messagebox.showinfo("Success", "Account created. You can now log in.")
            self.show_login()
        except AuthError as error:
            messagebox.showerror("Registration failed", str(error))

    def show_home(self):
        self.clear()
        user = self.auth.current_user
        tk.Label(self.root, text="Welcome to Phone Book",
                 font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Logged in as: {user['username']}").pack(pady=5)
        tk.Button(self.root, text="Update Profile", width=25,
                  command=self.show_profile).pack(pady=10)
        tk.Button(self.root, text="Log Out", width=25,
                  command=self.do_logout).pack(pady=5)
        tk.Label(self.root, text=(
            "Contact and Group screens will be connected\n"
            "by the other team members."
        ), fg="gray").pack(pady=25)

    def show_profile(self):
        self.clear()
        user = self.auth.current_user
        tk.Label(self.root, text="Update Profile",
                 font=("Arial", 18, "bold")).pack(pady=20)
        self.profile_username = self.make_label_entry(self.root, "Username")
        self.profile_username.insert(0, user["username"])
        self.profile_email = self.make_label_entry(self.root, "Email")
        self.profile_email.insert(0, user["email"])
        tk.Button(self.root, text="Save Changes", width=25,
                  command=self.do_update_profile).pack(pady=15)
        tk.Button(self.root, text="Cancel",
                  command=self.show_home).pack()

    def do_update_profile(self):
        try:
            self.auth.update_profile(
                self.profile_username.get(), self.profile_email.get()
            )
            messagebox.showinfo("Success", "Profile updated.")
            self.show_home()
        except AuthError as error:
            messagebox.showerror("Update failed", str(error))

    def do_logout(self):
        self.auth.logout()
        self.show_login()
