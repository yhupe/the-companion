import json
import os


class MessageHandling:
    def __init__(self):
        self.storage = "../data_base/message_history.json"
        self.local_data = self.load_storage()  # Load data on initialization

    def load_storage(self):
        """Loads message history from JSON file, handles missing or corrupt files."""
        if not os.path.exists(self.storage):
            return {}  # Return empty dictionary if file does not exist

        try:
            with open(self.storage, "r") as fobj:
                return json.load(fobj)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}  # Return empty dictionary if file is empty or corrupted

    def write_storage(self):
        """Writes the local_data dictionary to the JSON file."""
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, message_dict, whatsapp_nr):
        """Appends a message under the given WhatsApp number."""
        if whatsapp_nr not in self.local_data:
            self.local_data[whatsapp_nr] = []  # Initialize list if not present
        self.local_data[whatsapp_nr].append(message_dict)
        self.write_storage()


if __name__ == '__main__':
    data_handler = MessageHandling()

    new_message = {
        "Date": "2025-02-02",
        "Body": "message"
    }
    whatsapp_nr = "einszweidrei"

    data_handler.append_storage(new_message, whatsapp_nr)