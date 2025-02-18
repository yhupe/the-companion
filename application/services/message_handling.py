import json
import os
from pathlib import Path
from datetime import datetime


class MessageHandling:
    def __init__(self):
        storage_path = Path(__file__).parent.parent

        self.storage = storage_path / "data_base" / "message_history.json"
        print(self.storage)
        self.load_storage()

    def load_storage(self):
        """Loads message history from JSON file, handles missing or corrupt files."""
        if not os.path.exists(self.storage):
            self.local_data = {}  # Initialize if file doesn't exist

        try:
            with open(self.storage, "r") as fobj:
                self.local_data = json.load(fobj)
                print("Data loaded from file:", self.local_data)
        except (json.JSONDecodeError, FileNotFoundError):
            self.local_data = {}  # Reset data if file is corrupt or missing
            print("Error loading file. Initialized empty data.")

    def append_storage(self, message_dict, whatsapp_nr):
        """Appends a message under the given WhatsApp number, checking for duplicates."""
        if whatsapp_nr not in self.local_data:
            self.local_data[whatsapp_nr] = []

        # Check if the message with the same body and date already exists
        for msg in self.local_data[whatsapp_nr]:
            if msg['Body'] == message_dict['Body'] and msg['Date'] == message_dict[
                'Date']:
                print(
                    f"Duplicate message with body '{message_dict['Body']}' and date '{message_dict['Date']}' found. Skipping append.")
                return  # Skip appending if the message is a duplicate

        # Appending the new message
        self.local_data[whatsapp_nr].append(message_dict)

        # Writing the updated data to the file (this should append new entries, not overwrite)
        self.write_storage()

    def write_storage(self):
        """Writes the local_data dictionary to the JSON file."""
        # Before writing, print the data to check
        print("Saving data to file:", self.local_data)
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

