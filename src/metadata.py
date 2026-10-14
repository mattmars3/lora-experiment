import pickle

class ReceiverMeta:
    def __init__(self, args, total_payload_received, transmission_duration):
        self.args = args
        self.total_payload_received = total_payload_received
        self.transmission_duration = transmission_duration
        self.sender_location = ""
        self.receiver_location = ""
        self.estimated_distance = ""
        self.additional_notes = ""

    def write_recv_metadata(self, file_timestamp: str):
        filename = f"data/{file_timestamp}-recv-meta.pkl"
        with open(filename, "ab") as output:
            pickle.dump(self, output)

    @classmethod
    def read_recv_metadata(cls, file_timestamp: str):
        filename = f"data/{file_timestamp}-recv-meta.pkl"
        with open(filename, "rb") as file:
            return pickle.load(file)

    def prompt_and_add_additional_data(self):
        self.sender_location = input("Where is the sender located?: ")
        self.receiver_location = input("Where is the receiver located?: ")
        self.estimated_distance = input("What is the estimated distance?: ")
        self.additional_notes = input("Enter additional notes here: ")

