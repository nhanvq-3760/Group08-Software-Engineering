# Member 2 — Contact Management Testing Document

## 1. Objective

Verify Add/View/Search/Update/Delete Contact behavior, multi-user data separation, input validation, and SQLite referential integrity before integration with other members.

## 2. Test environment and method

- Language: Python >=3.10.
- Unit test tool: `unittest` (Python standard library).
- Repository integration: SQLite in-memory database and parameterized SQL.
- Database contract: `User`, `Contact`, `Phone_Number` from `database/schema_demo.sql`.
- Execution: `python -m unittest discover -s tests -v`.
- Network: not required.
- The test database is synthetic for functional testing. No production data is used.

## 3. Test case list

| ID | Feature | Input / action | Expected result |
|---|---|---|---|
| TC01 | Add | Valid contact + phone | Contact saved and assigned ID |
| TC02 | View | Two users own distinct contacts | Each user sees only own contacts |
| TC03 | View | Existing contact ID | Exact matching contact returned |
| TC04 | Search | Vietnamese mixed-case name | Accent/case-aware matching |
| TC05 | Search | Email/phone/address | Matching contact returned |
| TC06 | Update | Name/email/address | Values changed; ID remains |
| TC07 | Update | Replace and clear phones | Phone list updated correctly |
| TC08 | Delete | Existing contact | Contact and phone rows deleted |
| TC09 | Security | Other user's contact ID | View denied as not found |
| TC10 | Security | Other user's contact ID | Update denied |
| TC11 | Security | Other user's contact ID | Delete denied |
| TC12 | Validation | Blank full name | Validation error |
| TC13 | Validation | Invalid email | Validation error |
| TC14 | Validation | Invalid/duplicate phones | Validation error |
| TC15 | DB integrity | Unknown `user_id` | Foreign-key/validation error |
| TC16 | Security | SQL-like name text | Stored as text; database unaffected |
| TC17 | Delete | Nonexistent contact ID | Not found error |
| TC18 | Validation | Invalid identifiers | Validation error |
| TC19 | Integration boundary | Client sends forged user_id | Ignored; session user ID enforced |
| TC20 | Security | Search other user's name | No cross-user data leak |
| TC21 | Search | Blank query | List own contacts |
| TC22 | Validation | Duplicate phone input | Existing records unchanged |
| TC23 | DB integrity | Delete sample User | Contacts and phones cascade |
| TC24 | Search | No matching name | Empty list returned |

## 4. Acceptance criteria

All 24 test cases pass without errors. Member 2 code should not accept a user ID directly from an unverified client as evidence of identity. Database table/column alignment and end-to-end web/API behavior require later team integration testing.

## 5. Test evidence

Actual console output and Python version are saved in `docs/TEST_RESULTS.txt`. Testing was performed in the provided environment; the other members' source and the target Windows machine are not available for end-to-end testing.
