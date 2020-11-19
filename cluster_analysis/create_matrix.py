import json
import sys

sys.path.append("..")
from chat_file import ChannelFile


def create_hopped_dict(hopped_list):
    hopped_dict = {}  # hopped from : { hopped to : count }
    for hopped in hopped_list:
        finished = False
        while not finished:
            message = hopped.next()
            if not message:
                finished = True
                continue

            from_ = message.hopped_from
            to = message.hopped_to

            if from_ not in hopped_dict:
                hopped_dict[from_] = {}
            if to not in hopped_dict[from_]:
                hopped_dict[from_][to] = 0
            hopped_dict[from_][to] += 1

    return hopped_dict


if __name__ == '__main__':
    hopped = ChannelFile("../hopped_messages.json", custom_json=True)
    hopped_dict = create_hopped_dict([hopped])
    json.dump(hopped_dict, open("hopped_dict.json", "w"))
