
import sys
import tkinter as tk
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTACT_MANAGEMENT_PATH = PROJECT_ROOT / "ContactManagement"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(1, str(PROJECT_ROOT))

sys.path.insert(0, str(CONTACT_MANAGEMENT_PATH))

from presentation.auth_views import AuthApp
from database.connection import initialize_database, get_connection
from contact_management.auth_integration import initialize_contact_tables


def main():
    initialize_database()

    conn = get_connection()
    try:
        initialize_contact_tables(conn)
    finally:
        conn.close()

    root = tk.Tk()
    AuthApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
