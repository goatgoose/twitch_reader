from chat_message import ChatMessage
import json


class ChannelFile:
    def __init__(self, path):
        self.path = path

        self.file = open(path, "r")

    def next(self):
        line = self.file.readline()
        if not line:
            return None

        obj = None
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return None

        message = ChatMessage(obj)
        message.parse_twitch()
        return message
