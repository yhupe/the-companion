import json

class MedicationHandling:
    def __init__(self):
        path = "../db/medication.json"
        self.storage = path
        print(self.storage)
        self.local_data = []

    def load_storage(self):
        with open(self.storage, "r") as fobj:
            self.local_data = json.load(fobj)

    def write_storage(self):
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, medication_dict: dict):
        self.local_data.append(medication_dict)
        self.write_storage()



if __name__ == '__main__':
    data_1 = MedicationHandling()
    data_1.load_storage()

    data = {
        "WHATSAPP_NR": {
            "Medication_name": "Marihuana",
            "Dose": "1g",
            "Frequency": "1x/day",
            "Time": "10.00 pm"}
    }

    data_1.append_storage(data)
