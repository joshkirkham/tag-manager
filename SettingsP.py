"""
The settings process is responsible for managing the databases settings and reading them from
/db_files/settings during database start time

Each setting is stored as a key value pair in the settings file, in the format:
KEY=Value
"""

class SettingsP:
    def __init__(self, settings_file_path):
        self.settings = {}
        self.settings_file_path = settings_file_path

        try:
            file = open(settings_file_path, 'r')

            # Read the settings into a dictionary
            lines = file.readlines()
            for line in lines:
                if "=" in line:
                    kv_pair = line.split("=")
                    self.settings[kv_pair[0]] = kv_pair[1]

            file.close()

        except FileNotFoundError:
            print("ERROR: Cannot find database settings file. Exiting.")
            exit(2)




    def resolve(self, key):
        """
        Resolves a key in the settings to the proper value
        :return: The value as a string, if the value exists, an empty string otherwise
        """
        try:
            return self.settings[key]
        except ValueError:
            return ""


    def change_setting(self, key, new_value):
        """
        Changes an existing key to a new value
        :param new_value:  Must be a String
        :return: True if the value was changed, False if not
        """
        try:
            self.settings[key] = new_value
            return True
        except ValueError:
            return False



    def write_settings_to_file(self):
        """Write the current settings dictionary to the settings file"""
        file = open(self.settings_file_path, 'w')
        for key, val in self.settings.items():
            file.write(key + "=" + val)
        file.close()


    def close(self):
        """Actions to prepare for the process being ended"""
        self.write_settings_to_file()


