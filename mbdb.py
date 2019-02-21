import json

'''
Instructions:
1. Initilize database object.
mydb = MBDataBase()
2. add members
mydb.create_user(id, userdata)
id = string with user id
userdata = dictionary with user information, ex:
 {
 'name': 'bob',
 'RSVP': False,
 }
 
3. delete members
mydb.delete_user(id)
4. access member data:
user = mydb.get_user(id)
5. see your database
print(mydb)
6. update information
user = mydb.get_user(id)
update user fields here, call it updated_data
user.update_user(id, updated_data)
7. back up your database by using the save to file function
mydb.backup_database('backup file')
8. load a backup into a database
newdd = MBDataBase()
newdd.load_database('name of backup')
'''


class MBDataBase():
    user_list = {}
    fname = ''

    def __init__(self, fname='mydb'):
        self.fname = fname

    def __repr__(self):
        """
        This function creates a string object for the database.
        :return: string representation of the database.
        """
        s = 'Database: %s\n' % self.fname

        for id, u in self.user_list.items():
            s += str('%s:\n' % id)

            for field, elem in u.items():
                s += str('\t%s: %s\n' % (field, elem))

        return s

    def del_user(self, sender_id):
        """
        Deletes a user by sender_id from the database, and saves changes to file.
        :param sender_id: sender_id to delete.
        :return: True if success, else False.
        """
        if sender_id not in self.user_list:
            return False
        else:
            del self.user_list[sender_id]
            self.save_database()
            return True

    def update_user(self, sender_id, updated_data):
        """
        Updates user information into database. Saves changes to file.
        :param sender_id: the sender_id to update.
        :param updated_data: the updated fields of the user.
        :return: True if successful, else return False.
        """
        if sender_id not in self.user_list:
            return False

        self.user_list[sender_id] = updated_data
        self.save_database()
        return True

    def create_user(self, sender_id, user_data):
        """
        Creates a new user in the database. Saves changes to file.
        :param sender_id:
        :param user_data:
        :return:
        """
        if sender_id in self.user_list:
            return False

        self.user_list[sender_id] = user_data
        self.save_database()
        return True

    def get_user(self, sender_id):
        """
        Retrieve user data from the database.
        :param sender_id: id to search for.
        :return: user data, False if not found in db.
        """
        if sender_id not in self.user_list:
            return False
        else:
            return self.user_list[sender_id]

    def save_database(self):
        """
        Saves the database to file (disk). The name of the file is stored in MSDataBase.fname field.
        :return: No return, writes to disk.
        """
        with open(self.fname, 'w') as f:
            json.dump(self.user_list, f)

    def backup_database(self, fname):
        """
        Saves a copy of the database to file (disk). The name of the target file is specified by the function.
        :param fname: name of backup file.
        :return: No return, writes to disk.
        """
        with open(fname, 'w') as f:
            json.dump(self.user_list, f)

    def load_database(self, fname):
        """
        Loads a database from disk. The database must exist in a file specified by the fileanme. Can also be a valid
        path.
        :param fname: name fo file to read from.
        :return: No return, loads data into the object.
        """
        self.fname = fname
        with open(fname, 'r') as f:
            self.user_list = json.load(f)
