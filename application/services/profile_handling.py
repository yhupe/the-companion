import json
import os
from pathlib import Path

class ProfileHandling:
    def __init__(self):
        storage_path = Path(__file__).parent.parent
        self.local_data = {}
        self.storage = storage_path / "data_base" / "profile.json"
        self.load_storage()


    def load_storage(self):
        """Loads message history from JSON file, handles missing or corrupt files."""
        if not os.path.exists(self.storage):
            self.local_data = {}

        try:
            with open(self.storage, "r") as fobj:
                self.local_data = json.load(fobj)
                print("Data loaded from file:")
        except (json.JSONDecodeError, FileNotFoundError):
            self.local_data = {}
            print("Error loading file. Initialized empty data.")

    def append_storage(self, message_dict, whatsapp_nr):
        """Appends a message under the given WhatsApp number, checking for duplicates."""
        if whatsapp_nr not in self.local_data:
            self.local_data[whatsapp_nr] = [message_dict]
            self.write_storage()

        else:
            print("Number already registered")


    def write_storage(self):
        """Writes the local_data dictionary to the JSON file."""

        print("Saving data to file:", self.local_data)
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)




if __name__ == '__main__':
    data_1 = ProfileHandling()
    data_1.load_storage()
    whatsapp = "whatsapp-doc"
    data = {
        "WHATSAPP_NR": {
            "Date": "2024-02-02",
            "user_name": "Franz",
    }}

    data_1.append_storage(data, whatsapp_nr=whatsapp)

