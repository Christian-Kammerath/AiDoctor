from fastapi import HTTPException
from server.tokens import verify_token, create_jwt, is_token_owner_admin
from server.hashPassword import hashes_password
from loadSettings import get_settings
from server.dataBase import DataBase


# class to manage, create, manage and verify tokens
class SecurityCheck:
    def __init__(self, user_name="", password="", is_admin=False):
        self.security_settings = get_settings.select('security', 'token')
        self.user_name = user_name
        self.password = password
        self.is_admin = is_admin
        self.is_admin = self.check_is_admin()

    # returns whether user is registered as admin in the database
    def check_is_admin(self):
        return DataBase('userDb').select('user', 'isAdmin', 'userName = ?', (self.user_name,))

    # checks if password matches the hashed password in the database from the user and returns a token
    def check_security(self):

        if self.is_token_enabled():
            if self.password_checker():
                return {'access_permitted': True, 'token': create_jwt(self.user_name)}
            else:
                return {'access_permitted': False}
        return {'access_permitted': True}

    # checks if security is activated in the settings
    def is_token_enabled(self):
        if self.security_settings['token_enabled']:
            return True
        return False

    # reads the user's hashed password from the database and returns it
    def get_password_hash_from_db(self):
        db = DataBase('userDb')

        password_hash_from_db = db.select('user', 'passwordHash', 'userName = ?', (self.user_name,))

        if not password_hash_from_db:
            raise ValueError("Invalid username or password")
        return password_hash_from_db

    # hashes the given password and returns it
    def get_hash_from_password(self):
        return hashes_password(self.password)

    # checks whether the passed password matches the one in the database
    def password_checker(self):

        hash_from_db = self.get_password_hash_from_db()
        new_hash = self.get_hash_from_password()

        if hash_from_db[0][0] == new_hash:
            return True
        return False

    # checks if token is valid
    def is_user_token_valid(self, token=""):
        try:
            if self.is_token_enabled():
                if verify_token(token):
                    return True
                return False
            return True
        except HTTPException as e:
            if e.status_code == 401:
                return False

    # checks if admin token is valid
    def is_admin_token_valid(self, token=""):
        if self.is_token_enabled():
            if is_token_owner_admin(token):
                return True
            return False
        return True
