from server.dataBase import DataBase
from getpass import getpass
from server.hashPassword import hashes_password


def create_table(db):
    db.create_table('user', ["ID INTEGER PRIMARY KEY AUTOINCREMENT",
                             'firstName TEXT',
                             'lastName TEXT',
                             'userName TEXT UNIQUE',
                             'isAdmin BOOLEAN',
                             'passwordHash TEXT'])


def get_admin_user(db):
    return db.select('user', 'isAdmin', 'isAdmin = ?', (True,))


def insert_admin_in_db(db, first_name, last_name, user_name, hash_password):
    return db.insert('user', 'firstName, lastName, userName, isAdmin, passwordHash',
                     first_name, last_name, user_name, True, hash_password)


# checks whether an admin exists in the user database, if not a dialog is created to create one.

def start():
    db = DataBase('userDb')
    create_table(db)

    is_admin_user = get_admin_user(db)

    if len(is_admin_user) < 1:
        print("The token settings are activated. To start, it requires at least one admin user. Please create an "
              "initial admin user.")

        first_name = input('first name: ')
        last_name = input('last_name: ')
        user_name = input('user_name: ')
        password = getpass('password: ')
        hash_password = hashes_password(password)

        insert_admin_in_db(db, first_name, last_name, user_name, hash_password)
        return True

    return True
