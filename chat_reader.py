import os
from chat_message import ChatMessage
from channel_file import ChannelFile
import json
import numpy as np
import sys
import time


class ChatReader:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.blacklisted_users = {"nightbot", "streamelements", "fossabot", "streamlabs"}

    def replay(self):
        channels = []
        for root, dirs, files in os.walk(self.data_dir):
            for name in files:
                path = os.path.join(root, name)
                if not path.endswith(".json"):
                    continue
                channels.append(ChannelFile(path))

        last_channel = {}  # user : last active channel name
        next_messages = [f.next() for f in channels]
        while True:
            min_timestamp = float("inf")
            min_index = -1
            all_eof = True
            for i, message in enumerate(next_messages):
                if message:
                    all_eof = False
                else:
                    continue
                if message.timestamp < min_timestamp:
                    min_timestamp = message.timestamp
                    min_index = i
            if all_eof:
                break

            min_message = next_messages[min_index]
            min_channel = channels[min_index]

            user = min_message.user

            if user not in self.blacklisted_users:
                if user not in last_channel:
                    last_channel[user] = min_message.channel
                if min_message.channel != last_channel[user]:
                    if user not in self.blacklisted_users:
                        print(f"[{min_message.timestamp}] {last_channel[user]} -> {min_message.channel} [{user}]: {min_message.content}")
                        last_channel[user] = min_message.channel

            next_messages[min_index] = min_channel.next()


if __name__ == '__main__':
    reader = ChatReader("../chat_data/data1")
    reader.replay()
