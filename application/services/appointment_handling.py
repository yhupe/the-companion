import json

class AppointmentHandling:
    def __init__(self):
        path = "../db/appointment.json"
        self.storage = path
        print(self.storage)
        self.local_data = []

    def load_storage(self):
        with open(self.storage, "r") as fobj:
            self.local_data = json.load(fobj)

    def write_storage(self):
        with open(self.storage, "w") as fobj:
            json.dump(self.local_data, fobj, indent=4)

    def append_storage(self, appointment_dict: dict):
        self.local_data.append(appointment_dict)
        self.write_storage()



if __name__ == '__main__':
    data_1 = AppointmentHandling()
    data_1.load_storage()

    data = {
        "WHATSAPP_NR": {
            "Appointment_title": "Cardiology",
            "Date": "2025-02-20",
            "Time": "9.00 am",
            "Place": "Hospital"}
    }

    data_1.append_storage(data)
