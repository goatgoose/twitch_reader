from chat_message import ChatMessage
import json


class ChannelFile:
    def __init__(self, path, custom_json=False):
        self.path = path
        self.custom_json = custom_json

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
        if self.custom_json:
            message.parse_custom()
        else:
            message.parse_twitch()
        return message
