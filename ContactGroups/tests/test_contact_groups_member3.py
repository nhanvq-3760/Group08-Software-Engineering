import sqlite3, unittest
from contact_groups import SQLiteGroupRepository, ContactGroupService, GroupValidationError, GroupNotFound, ContactNotFound

SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE "User"(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL);
CREATE TABLE "Contact"(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, full_name TEXT NOT NULL, email TEXT DEFAULT '', address TEXT DEFAULT '', FOREIGN KEY(user_id) REFERENCES "User"(id) ON DELETE CASCADE);
CREATE TABLE "Contact_Group"(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,group_name TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES "User"(id) ON DELETE CASCADE, UNIQUE(user_id,group_name));
CREATE TABLE "Contact_Group_Member"(group_id INTEGER NOT NULL,contact_id INTEGER NOT NULL,PRIMARY KEY(group_id,contact_id),FOREIGN KEY(group_id) REFERENCES "Contact_Group"(id) ON DELETE CASCADE,FOREIGN KEY(contact_id) REFERENCES "Contact"(id) ON DELETE CASCADE);
'''
class ContactGroupTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:'); self.db.executescript(SCHEMA)
        self.db.executemany('INSERT INTO "User" VALUES (?,?)',[(1,'alice'),(2,'bob')])
        self.db.executemany('INSERT INTO "Contact"(id,user_id,full_name,email,address) VALUES (?,?,?,?,?)',[(11,1,'An','an@x',''),(12,1,'B├¼nh','binh@x',''),(21,2,'Bob','bob@x','')])
        self.s=ContactGroupService(SQLiteGroupRepository(self.db))
    def tearDown(self): self.db.close()
    def test_create_and_trim_name(self):
        g=self.s.create(1,'  Family  '); self.assertEqual(g.group_name,'Family'); self.assertGreater(g.id,0)
    def test_list_is_user_scoped(self):
        self.s.create(1,'Family'); self.s.create(2,'Family'); self.assertEqual(len(self.s.list(1)),1); self.assertEqual(len(self.s.list(2)),1)
    def test_create_blank_rejected(self):
        with self.assertRaises(GroupValidationError):self.s.create(1,'  ')
    def test_name_too_long_rejected(self):
        with self.assertRaises(GroupValidationError):self.s.create(1,'x'*51)
    def test_duplicate_name_rejected_per_user(self):
        self.s.create(1,'Friends')
        with self.assertRaises(GroupValidationError):self.s.create(1,'Friends')
    def test_same_name_allowed_for_different_users(self):
        self.s.create(1,'Friends'); self.s.create(2,'Friends'); self.assertEqual(len(self.s.list(2)),1)
    def test_rename(self):
        g=self.s.create(1,'Old'); new=self.s.rename(1,g.id,'New'); self.assertEqual(new.group_name,'New')
    def test_rename_duplicate_rejected(self):
        a=self.s.create(1,'A'); self.s.create(1,'B')
        with self.assertRaises(GroupValidationError):self.s.rename(1,a.id,'B')
    def test_delete_group_removes_membership_not_contact(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,11); self.s.delete(1,g.id)
        with self.assertRaises(GroupNotFound): self.s.view(1,g.id)
        self.assertIsNotNone(self.db.execute('SELECT id FROM Contact WHERE id=11').fetchone())
        self.assertEqual(self.db.execute('SELECT count(*) FROM Contact_Group_Member').fetchone()[0],0)
    def test_view_group_and_members(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,11); self.assertEqual(self.s.view(1,g.id).contacts[0]['full_name'],'An')
    def test_add_contact(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,12); self.assertEqual(len(self.s.view(1,g.id).contacts),1)
    def test_duplicate_membership_rejected(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,11)
        with self.assertRaises(GroupValidationError):self.s.add_contact(1,g.id,11)
    def test_contact_other_user_rejected(self):
        g=self.s.create(1,'G')
        with self.assertRaises(ContactNotFound):self.s.add_contact(1,g.id,21)
    def test_group_other_user_rejected(self):
        g=self.s.create(1,'G')
        with self.assertRaises(GroupNotFound):self.s.add_contact(2,g.id,21)
    def test_remove_member(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,11); self.s.remove_contact(1,g.id,11); self.assertEqual(len(self.s.view(1,g.id).contacts),0)
    def test_remove_nonmember_rejected(self):
        g=self.s.create(1,'G')
        with self.assertRaises(GroupNotFound):self.s.remove_contact(1,g.id,11)
    def test_contact_delete_cascades_membership(self):
        g=self.s.create(1,'G'); self.s.add_contact(1,g.id,11); self.db.execute('DELETE FROM Contact WHERE id=11'); self.db.commit()
        self.assertEqual(len(self.s.view(1,g.id).contacts),0)
    def test_invalid_user_id(self):
        with self.assertRaises(GroupValidationError):self.s.list(0)
    def test_invalid_group_id(self):
        with self.assertRaises(GroupValidationError):self.s.view(1,-2)
    def test_sql_injection_string_is_stored_safely(self):
        name="Friends'; DROP TABLE Contact;--"; self.s.create(1,name)
        self.assertIsNotNone(self.db.execute('SELECT * FROM Contact').fetchone())
        self.assertEqual(self.s.list(1)[0].group_name,name)
    def test_group_not_found(self):
        with self.assertRaises(GroupNotFound):self.s.rename(1,999,'Nope')
    def test_empty_groups_list(self):
        self.assertEqual(self.s.list(1),[])
if __name__=='__main__':unittest.main()
