from pathlib import Path
import json

class ProfileHandling:
    def __init__(self):
        path = "../data_base/profile.json"
        self.storage = path
        print(self.storage)
        self.local_data = []

    def load_storage(self):
        with open(self.storage, "r") as fobj:
            self.local_data = json.load(fobj)

    def write_storage(self):
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, profile_dict: dict):
        self.local_data.append(profile_dict)
        self.write_storage()


if __name__ == '__main__':
    data_1 = ProfileHandling()
    data_1.load_storage()

    data = {
        "WHATSAPP_NR": {
            "Date": "2024-02-02",
            "From": "from whatsapp +12234214",
            "Name": "Suzanna Sum",
            "Age": "78"}
    }

    data_1.append_storage(data)

