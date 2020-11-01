import os
from chat_message import ChatMessage
from channel_file import ChannelFile
from chat_context import ChatContext
import json
import numpy as np
import sys
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

sid = SentimentIntensityAnalyzer()


class ChatReader:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.blacklisted_users = {"nightbot", "streamelements", "fossabot", "streamlabs", "moobot"}

    def write_hopped(self):
        chat_contexts = {}  # user : last active channel name

        for message in self.replay():
            user = message.user

            if user not in self.blacklisted_users:
                if user not in chat_contexts:
                    chat_contexts[user] = ChatContext(user)
                chat_context = chat_contexts[user]
                chat_context.log_message(message)

                most_common_channel, occurrences = chat_context.active_channel
                if message.channel != most_common_channel:
                    if occurrences > 2:
                        sentiment_score = sid.polarity_scores(message.content)
                        message.hopped_from = most_common_channel
                        message.hopped_to = message.channel
                        message.messages_in_from = occurrences
                        message.vader_score = sentiment_score

                        dt = datetime.fromtimestamp(message.timestamp)
                        print(f"[{dt}] {message.hopped_from} "
                              f"({message.messages_in_from}) -> {message.hopped_to} [{message.user}] "
                              f"({message.vader_score['compound']}): {message.content}")
                        with open(f"hopped_messages.json", "a+") as hopped_file:
                            hopped_file.write(message.to_custom_json() + "\n")

    def replay(self):
        channels = []
        for root, dirs, files in os.walk(self.data_dir):
            for name in files:
                path = os.path.join(root, name)
                if not path.endswith(".json"):
                    continue
                channels.append(ChannelFile(path))

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

            yield min_message

            next_messages[min_index] = min_channel.next()


if __name__ == '__main__':
    reader = ChatReader("../chat_data/data1")
    reader.write_hopped()
