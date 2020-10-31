import os
from chat_message import ChatMessage
import json
import numpy as np
import sys


class ChatReader:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.arr = np.memmap("memmap.dat", mode="w+", shape=(1, 1), dtype="U1200")

    def write_to_file(self, out):
        count = 0
        for root, dirs, files in os.walk(self.data_dir):
            for file_name in files:
                path = os.path.join(root, file_name)
                if not path.endswith(".json"):
                    continue

                print(f"reading from: {path}")
                with open(path, "r") as message_file:
                    for line in message_file.readlines():
                        try:
                            np.append(self.arr, line)
                            count += 1
                        except json.JSONDecodeError:
                            print(f"invalid json: {line}")
        print(self.arr[0:10])
        del self.arr


if __name__ == '__main__':
    reader = ChatReader("../chat_data")
    reader.write_to_file("chat_data.json")
