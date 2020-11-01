from chat_message import ChatMessage
from chat_block import ChatBlock
import json
from abc import ABCMeta, abstractmethod


class ChatFile:
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path

        self.file = open(path, "r")

    def _next(self):
        line = self.file.readline()
        if not line:
            return None

        obj = None
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return None

        return obj

    @abstractmethod
    def next(self):
        pass


class ChannelFile(ChatFile):
    def __init__(self, path, custom_json=False):
        super().__init__(path)

        self.custom_json = custom_json

    def next(self):
        obj = self._next()

        message = ChatMessage(obj)
        if self.custom_json:
            message.parse_custom()
        else:
            message.parse_twitch()
        return message


class BlockFile(ChatFile):
    def __init__(self, path):
        super().__init__(path)

    def next(self):
        obj = self._next()
        block = ChatBlock.from_obj(obj)
        return block