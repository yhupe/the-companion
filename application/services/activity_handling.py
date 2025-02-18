import json

class ActivityHandling:
    def __init__(self):
        path = "../data_base/activity.json"
        self.storage = path
        print(self.storage)
        self.local_data = []

    def load_storage(self):
        with open(self.storage, "r") as fobj:
            self.local_data = json.load(fobj)

    def write_storage(self):
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, activity_dict: dict):
        self.local_data.append(activity_dict)
        self.write_storage()



if __name__ == '__main__':
    data_1 = ActivityHandling()
    data_1.load_storage()

    data = {
        "WHATSAPP_NR": {
            "Activity_title": "Choir",
            "Date": "2025-02-20",
            "Time": "5.00 pm",
            "Place": "Church"}
    }

    data_1.append_storage(data)