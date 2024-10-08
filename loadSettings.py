import json


# a small help class for reading, changing and copying settings
class Settings:
    def __init__(self, path):
        self.path = path
        self.settings = {}

    # reads setting from json file saves it in dictionary and returns it
    def load_settings(self):
        with open(self.path, 'r') as file:
            self.settings = json.load(file)

        return self

    # add new entry
    def add_value(self, key, value):
        self.settings[key] = value

    # change entry value
    def change_value(self, key, new_value):
        self.settings[key] = new_value
        with open(self.path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    # Copies part of settings into another json file
    def copy_setting_entry_to_other_file(self, target_path, *key):
        to_copy_value = self.select(*key)

        new_dic = {key[0]: to_copy_value}

        with open(target_path, 'w') as file:
            json.dump(new_dic, file, indent=4)

    # selects an entry
    def select(self, *key):
        last_select = self.settings

        try:
            for i in key:
                last_select = last_select[i]
        except (KeyError, TypeError) as e:
            raise ValueError(f"Invalid key sequence: {' -> '.join(map(str, key))}") from e

        return last_select


get_settings = Settings('settings.json').load_settings()
