import tkinter as tk
from presentation.auth_views import AuthApp
from database.connection import initialize_database

def main():
    initialize_database()
    root = tk.Tk()
    AuthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
