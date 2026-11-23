# Testing draft — Member 4
Use the lecturer's official Elearning 5 Testing Document Template for final submission.
The cases below are draft test scenarios, not a replacement for that template.

| ID | Feature | Test | Expected result |
|---|---|---|---|
| DB-01 | Schema | Initialize database | Five required tables exist |
| DB-02 | Foreign key | Insert Contact with nonexistent User ID | Insert is rejected |
| DB-03 | Cascade | Delete a User with related Contacts | Related records follow approved cascade policy |
| DB-04 | Integrity | Run foreign_key_check and integrity_check | No FK errors; integrity result is `ok` |
| ADM-01 | View users | Admin opens user list | User accounts are displayed without password hashes |
| ADM-02 | Deactivate | Admin deactivates an active user | is_active becomes 0 |
| ADM-03 | Activate | Admin activates an inactive user | is_active becomes 1 |
| ADM-04 | Delete self | Admin attempts to delete own account | Operation is rejected |
| ADM-05 | Duplicate | Create account with duplicate email | Database rejects duplicate email |
| SEC-01 | Password | Hash a password | Stored value is not plain text |
| SEC-02 | Verification | Verify correct / incorrect password | Correct succeeds; incorrect fails |
| INT-01 | Integration | Login as normal user and request Admin screen | Access must be denied by authentication/authorization layer |
