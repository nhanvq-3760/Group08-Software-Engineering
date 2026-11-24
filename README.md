# Phone Book Management System

## 1. Project Overview

The **Phone Book Management System** is a Python-based desktop application that allows users to manage personal contacts and organize them into contact groups.

The system provides user authentication, contact management, profile management, and administrative functionality. It uses SQLite for persistent data storage and Tkinter for the graphical user interface.

## 2. Main Features

### Authentication
- User Registration
- User Login and Logout
- Update User Profile
- Password Hashing

### Contact Management
- Add New Contacts
- View Contact List
- Search Contacts
- Update Contact Information
- Delete Contacts
- User Ownership Validation

### Contact Group Management
- Create Contact Groups
- View Contact Groups
- Rename Contact Groups
- Delete Contact Groups
- Add Contacts to Groups
- Remove Contacts from Groups

### Administration
- View User Accounts
- Create and Delete User Accounts
- Activate and Deactivate Accounts
- Change User Roles
- Password Hashing and Verification

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Main programming language |
| Tkinter | Graphical User Interface |
| SQLite | Database management |
| pytest | Automated testing |
| unittest | Unit and integration testing |
| Docker | Application containerization |
| Git & GitHub | Version control and collaboration |

## 4. Project Structure

```text
Group08-Software-Engineering/
│
├── Authentication/
│   ├── business/
│   ├── database/
│   ├── data_access/
│   ├── presentation/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
│
├── ContactManagement/
│   ├── contact_management/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── ContactGroups/
│   ├── contact_groups/
│   ├── database/
│   ├── presentation/
│   └── tests/
│
├── admin/
│   ├── admin_gui.py
│   ├── admin_service.py
│   ├── database.py
│   ├── security.py
│   └── tests/
│
├── Dockerfile
├── .dockerignore
└── README.md
```

## 5. Requirements

- Python 3.10 or later
- Docker Desktop (for Docker execution)
- Windows operating system for the desktop GUI setup

## 6. Run the Application Locally

Clone the repository:

```bash
git clone https://github.com/nhanvq-3760/Group08-Software-Engineering.git
```

Navigate to the project directory:

```bash
cd Group08-Software-Engineering
```

Run the application:

```bash
python Authentication/main.py
```

The application initializes the SQLite database automatically when started.

## 7. Docker Setup and Execution

The project includes a root-level Dockerfile for running the main application in a container.

### Build Docker Image

```bash
docker build -t phonebook-system .
```

### Run Docker Container on Windows

The application uses Tkinter, so an X Server such as VcXsrv is required to display the GUI on Windows.

Start VcXsrv with XLaunch and enable Disable access control.

Run:

```powershell
docker run --rm -it `
  -e DISPLAY=host.docker.internal:0.0 `
  -v "${PWD}/Authentication:/app/Authentication" `
  phonebook-system
```

The database directory is mounted from the host machine to preserve SQLite data outside the container.

## 8. Testing

Run Authentication tests:

```bash
python -m pytest Authentication/tests/ -v
```

Run Contact Management tests:

```bash
python -m unittest discover -s ContactManagement/tests -v
```

Run Contact Group tests:

```bash
python -m pytest ContactGroups/tests/ -v
```

Run Admin tests:

```bash
python -m pytest admin/ -v
```

## 9. Team Responsibilities

| Member | Responsibilities |
|---|---|
| Member 1 | Authentication, User Profile, and System Integration |
| Member 2 | Contact Management |
| Member 3 | Contact Group Management |
| Member 4 | Database Design, Administration, and Testing |

## 10. Database

The system uses SQLite to store user accounts, contacts, and contact groups.

The main database is located at:

```text
Authentication/phonebook.db
```

The database schema uses foreign keys to maintain relationships and data integrity.

**Note:** Generated database files and personal user data should not be committed to GitHub.

---

**Group 08 – Software Engineering Project**