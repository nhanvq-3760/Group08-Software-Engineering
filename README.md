Phone Book Management Systerm 

Functional Requirements. 

1. Register Account 

The system allows visitors to register a new account. 

Users enter a username, email, password, and confirm password. 

The system checks if the username or email already exists. 

If the information is valid, a new account is created. 

If the information is invalid, the system displays an error message. 

2. Log In 

The system allows registered users and administrators to log in. 

Users enter their username or email and password. 

The system checks the login information. 

If the information is correct, users can access the system. 

If the information is incorrect, an error message is displayed. 

3. Add Contact 

The system allows users to add new contacts. 

Users enter the contact's name, phone number, email, address, and contact group. 

Name and phone number are required. 

The system generates a Contact ID automatically. 

Valid information is saved to the database. 

An error message is displayed if required information is missing. 

4. View Contacts 

The system allows users to view their saved contacts. 

Users can view all contacts in their phone book. 

Contacts are displayed alphabetically. 

Users can select a contact to view more details. 

If there are no contacts, the system displays a message. 

5. Search Contact 

The system allows users to search for contacts. 

Users enter a name or phone number. 

The system searches for matching contacts. 

Matching results are displayed. 

If no contact is found, the system displays a message. 

6. Update Contact 

The system allows users to edit contact information. 

Users select an existing contact. 

The system displays the current information. 

Users can change the name, phone number, email, address, and contact group. 

The system checks the updated information before saving. 

Users can cancel without saving changes. 

7. Delete Contact 

The system allows users to delete contacts. 

Users select a contact to delete. 

The system asks for confirmation. 

If the user confirms, the contact is deleted from the database. 

If the user cancels, the contact remains unchanged. 

8. Manage Contact Groups 

The system allows users to organize contacts into groups. 

Users can create new contact groups. 

Users can view existing groups. 

Users can rename or delete groups. 

Users can add contacts to one or more groups. 

Users can remove contacts from groups. 

Deleting a group does not delete its contacts. 

9. Update ProfileThe system allows users to update their account information. 

Users can view their profile information. 

Users can update their username or other editable information. 

The system checks the information before saving. 

Users can cancel the update. 

10. Log Out 

The system allows users to log out of their accounts. 

Users select the Log Out function. 

The system ends the current session. 

Users are returned to the login screen. 

11. Manage User Accounts 

The system allows administrators to manage registered user accounts. 

Administrators can view the list of users. 

Administrators can search for users by username or email. 

Administrators can update user account information. 

Administrators can delete user accounts after confirmation. 

The system displays a success or error message after each operation. 

NON-FUNCTIONAL REQUIREMENTS 

1. Usability 

The system shall provide a simple, intuitive, and user-friendly interface that allows users to manage their contacts easily. 

Main functions such as adding, viewing, searching, updating, and deleting contacts shall be clearly displayed and easily accessible. 

The system shall provide clear confirmation and error messages to help users understand the results of their actions. 

2. Reliability 

The system shall ensure that contact information is stored accurately and reliably in the database. 

The system shall preserve saved contact information after the application is closed and reopened. 

The system shall prevent data loss or corruption during normal operations. 

If an operation fails, the system shall display an error message and ensure that existing contact information remains unchanged. 

The system shall maintain data consistency when users add, update, or delete contacts and contact groups. 

3. Performance 

The system shall respond to common user operations, such as viewing, searching, and updating contacts, within 2 seconds under normal operating conditions. 

The system shall support storing and managing at least 1,000 contacts without significant performance degradation. 

The system shall retrieve contact information efficiently from the database. 

The system shall display search results promptly when users enter a contact name or phone number. 

4. Security 

The system shall require users to log in with valid credentials before accessing their personal contact information. 

User passwords shall be stored securely using a salted password-hashing algorithm rather than plain text. 

The system shall ensure that users can only access and manage their own contacts and contact groups. 

The system shall validate user input to prevent invalid or malicious data from being processed. 

The system shall protect the database against unauthorized access and SQL injection attacks. 

5. Maintainability (Supportability) 

The system shall follow a modular software architecture to make the source code easier to understand, maintain, and extend. 

The source code shall be organized into separate components with clearly defined responsibilities. 

The system shall allow developers to add new features or modify existing functions without significantly affecting other components. 

The development team shall use version control to manage source code changes and support collaboration. 

The system shall provide appropriate error information to assist developers in identifying and fixing defects. 

6. Design Constraints 

The system shall be developed using a programming language permitted by the course, such as Python, C++, or Java. 

The system shall use a relational database to store user accounts, contact information, phone numbers, and contact groups. 

The system shall provide a graphical user interface consistent with the approved GUI design. 

The database design shall define primary keys, foreign keys, and relationships to maintain data integrity. 

The system shall follow an appropriate software architecture or design pattern studied in the course. 

The project source code and documentation shall be maintained using GitHub or another suitable version control platform. 

7. Register Account 

The system allows new users to create an account with the following features: 

Users can register by entering a username, email address, and password. 

The system validates the entered information before creating an account. 

The system shall prevent registration with an existing username or email address. 

If the information is valid, the system creates a new account and displays a success message. 

If the information is invalid, the system displays an appropriate error message. 

8. Log In 

The system allows registered users to access their accounts with the following features: 

Users can enter their username or email address and password to log in. 

The system verifies the provided credentials. 

If the credentials are correct, the system allows the user to access their personal phone book. 

If the credentials are incorrect, the system displays an error message and denies access. 

9. Log Out 

The system allows authenticated users to log out of their accounts with the following features: 

Users can select the Log Out function to end their current session. 

The system terminates the user's active session. 

After logging out, the system redirects the user to the login screen. 

Users must log in again to access their personal contact information. 

 

DATA FLOW DIAGRAM (DFD). 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 USE CASE DIAGRAM 

 

1.1. Actor List (1 actor) 

No. 

Actor 

Description 

 

01 

Vistor 

 

 

A person who registers, logs in, and manages their personal contacts and contact groups 

 

02 

User 

View Contacts, Search Contact, Add Contact, Update Contact, Delete Contact, Manage Contact Groups, Log Out 

 

03 

Admin 

A system administrator who manages user accounts and system information. 

 

1.2. Use Case List (10 use cases) 

 

No. 

Use Case 

Description 

1 

Register Account 

Create a new user account. 

2 

Log In 

Access the system using valid credentials. 

3 

View Contacts 

Display saved contacts and their details 

4 

Search Contact 

 

Find contacts by name or phone number. 

5 

Add contact 

 

Create a new contact 

6 

Update Contact 

 

Modify existing contact information. 

7 

Delete Contact 

 

Remove a contact from the phone book. 

8 

Manage Contact Groups 

 

Create, rename, delete groups, and manage group members.  

 

9 

 

 

 
10 

Log Out 

 

Manage User Accounts 

 

End the current user session. 

 

 

Allow the administrator to view, update, and delete user accounts. 

 

 

 

 

 

V. CLASS DIAGRAM 

 

 

 

 

VI. DATABASE DESIGN 

1. Conceptual Database Diagram 

 

Logic Table 

User  

 

UserID 

UserName 

PassWord 

Email 

  

  

  

  

Contact 

  

ContactID 

FullName 

Email 

Address 

Note 

UserID 

  

  

  

  

  

(*) 

Phone_number 

  

PhoneID 

PhoneNumber 

ContactID 

  

  

(*) 

Contact_group_member 

  

MemberID 

GroupID 

ContactID 

  

(*) 

(*) 

Contact_group 

  

GroupID 

GroupName 

UserID 

  

  

(*) 

 

 

VII. INTERFACE DESIGN 

1.1. Login Screen 

The Login Screen allows registered users to access the Phone Book Management System by entering their email address and password. It also provides an option for new users to create an account. 

1.2. Contacts Screen 

The Register Account Screen allows new users to create an account by entering their username, email address, password, and confirm password. The system checks the information before creating the account. If the information is invalid, an error message will be displayed. 

1.3. Add Contact Screen 

The Add Contact Screen allows users to enter new contact information, including first name, last name, phone number, email address, home address, birthday, contact group, and notes. Users can save the new contact or cancel the operation. 

1.4. Edit Contact Screen 

The Edit Contact Screen displays the selected contact's current information and allows users to modify it. Users can save their changes or cancel the editing process. 

1.5. Contact Details Screen 

The Contact Details Screen displays detailed information about a selected contact, including their name, phone number, email address, home address, birthday, contact group, and notes. Users can return to the contact list, edit the contact, or delete it. 

1.6. Contact Groups Screen 

The Contact Groups Screen allows users to view and organize contacts into different groups, such as Family, Friends, Work, and School. Users can create new groups, view group members, and add contacts to groups. 

VIII. SOFTWARE ARCHITECTURE DESIGN 

1. Architecture Overview 

The Phone Book Management System is designed using a Layered Architecture to separate the system into different components with specific responsibilities. 

The system consists of three main layers: Presentation Layer, Business Logic Layer, and Data Access Layer. 

Presentation Layer: Provides the graphical user interface, allowing users to interact with the system through screens such as Login, Contacts, Add Contact, Edit Contact, and Contact Groups. 

Business Logic Layer: Processes user requests, validates contact information, handles authentication, and manages contacts and contact groups. 

Data Access Layer: Communicates with the database to store, retrieve, update, and delete information, including user accounts, contacts, phone numbers, and contact groups. 

This architecture improves maintainability, code organization, and scalability by separating user interface components from business logic and database operations. 

 

IX. SOFTWARE TESTING 

1. Testing Objectives 

The purpose of software testing is to check whether the Phone Book Management System works correctly and meets the project requirements. 

Testing focuses on the main functions, including registration, login, contact management, group management, and account management. 

2. Test Cases 

Test ID 

Test Case 

Expected Result 

TC01 

Register with valid information 

Account is created successfully 

TC02 

Register with an existing email 

Error message is displayed 

TC03 

Log in with correct information 

Login is successful 

TC04 

Log in with wrong password 

Access is denied 

TC05 

Add a contact with valid information 

Contact is saved 

TC06 

Add a contact without a name 

Error message is displayed 

TC07 

View contact list 

Saved contacts are displayed 

TC08 

Search for an existing contact 

Matching contacts are displayed 

TC09 

Search for a contact that does not exist 

No results message is displayed 

TC10 

Update contact information 

Contact information is updated 

TC11 

Delete contact and confirm 

Contact is deleted 

TC12 

Cancel contact deletion 

Contact remains unchanged 

TC13 

Create a new contact group 

Group is created 

TC14 

Delete a contact group 

Group is deleted but contacts remain 

TC15 

Update user profile 

Profile is updated 

TC16 

Log out of the system 

Session ends successfully 

TC17 

Admin deletes a user account 

Selected account is deleted 

TC18 

User tries to access another user's contacts 

Access is denied 

3. Unit Testing 

Unit testing is used to test individual functions of the system. 

The following functions should be tested: 

Contact creation and validation. 

Contact searching. 

Contact updating. 

Contact deletion. 

User authentication. 

Contact group management. 

For example, the Add Contact function should reject empty names and phone numbers. The Search Contact function should return matching contacts when a valid keyword is entered. 

Python pytest, Java JUnit, or another appropriate testing tool can be used depending on the programming language. 

4. Debugging 

During testing, errors may be found in the application. The development team should identify the causes and correct them. 

The debugging process includes: 

Identify the error. 

Reproduce the error. 

Check the related source code. 

Fix the problem. 

Run the test again. 

After fixing a problem, the related functions should be tested again to make sure the changes do not cause new errors. 

5. Defect Management 

The team should record and track errors found during testing. 

Bug ID 

Problem 

Severity 

Status 

BUG01 

Example: Contact can be saved without a name 

Medium 

Not verified 

BUG02 

Example: Search does not return an existing contact 

Medium 

Not verified 

BUG03 

Example: Deleting a group also removes contacts 

High 

Not verified 

The table above contains possible defects for testing purposes. Actual defects and their status must be updated after testing the application. 

6. Testing Results 

The team will record the actual results after executing the test cases. 

For each test case, the results should include: 

Expected Result 

Actual Result 

Pass or Fail 

Notes about any errors found 

The final testing report should summarize the number of passed and failed test cases and the defects that were fixed. 

 
