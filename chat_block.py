
class ChatBlock:
    def __init__(self, duration):
        self.duration = duration  # seconds

        self.messages = []
        self.harassed = []

    @staticmethod
    def from_obj(obj):
        pass

    def log_message(self, message):
        self.messages.append(message)

    def log_harassment(self, message):
        self.harassed.append(message)
