from collections import Counter


class ChatContext:
    MESSAGE_HISTORY_LEN = 10

    def __init__(self, user):
        self.user = user

        self.message_history = []

    def log_message(self, message):
        self.purge()
        self.message_history.append(message)
        if len(self.message_history) > self.MESSAGE_HISTORY_LEN:
            self.message_history.pop(0)

    @property
    def active_channel(self):
        counter = Counter([message.channel for message in self.message_history])
        return counter.most_common(1)[0]

    def purge(self):
        if len(self.message_history) == 0:
            return

        if self.message_history[0].timestamp < self.message_history[-1].timestamp - 60 * 60 * 3:
            self.message_history = []
