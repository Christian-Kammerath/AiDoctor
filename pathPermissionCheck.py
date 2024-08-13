import os
from loadSettings import get_settings
from server import securityCheck
from server import tokens


# is used to check the authorization of path accesses
class PathPermissionCheck:
    def __init__(self, path, token):
        self.path = path
        self.settings = get_settings.select('security', 'path_permission')
        self.token = token

    def is_path_public(self):
        public_path_allowed_list = self.settings['public_allowed_paths']
        return self.is_path_allowed(public_path_allowed_list)

    def is_path_user(self):
        user_allowed_path_list = self.settings['user_allowed_paths']
        return self.is_path_allowed(user_allowed_path_list)

    def is_path_admin(self):
        admin_allowed_path_list = self.settings['admin_allowed_paths']
        return self.is_path_allowed(admin_allowed_path_list)

    # checks whether the path is in the list of allowed accesses
    def is_path_allowed(self, allowed_list):
        abs_target_path = os.path.abspath(self.path)

        for allowed_dir in allowed_list:
            abs_allowed_dir = os.path.abspath(allowed_dir)

            if abs_target_path.startswith(abs_allowed_dir):
                return True

        return False

    # checks paths for their access rights and uses tokens to check whether the token owner is authorized.
    # The accesses are: Public (without restrictions), user (user and admin only), admin (admin only)
    def check(self):
        if self.is_path_public():
            return True
        elif self.is_path_user():
            if securityCheck.SecurityCheck().is_user_token_valid(self.token):
                return True
        elif self.is_path_admin():
            if securityCheck.SecurityCheck().is_admin_token_valid(self.token):
                return True
        return False
