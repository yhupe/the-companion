from pathlib import Path
import json

class DataHandling:
    def __init__(self):
        path = "../services/message_history.json"
        self.storage = "message_history.json"
        print(self.storage)
        self.local_data = {}

    def load_storage(self):
        with open(self.storage, "r") as fobj:
            self.local_data = json.load(fobj)

    def write_storage(self):
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, key, value):
        value = {}
        self.local_data[key] = value




if __name__ == '__main__':
    data_1 = Data_handling()
    data_1.load_storage()
