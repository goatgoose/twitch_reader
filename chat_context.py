from collections import Counter


class ChatContext:
    MESSAGE_HISTORY_LEN = 10

    def __init__(self, user):
        self.user = user

        self.channel_history = []

    def log_message(self, message):
        self.purge()
        self.channel_history.append((message.channel, message.timestamp))
        if len(self.channel_history) > self.MESSAGE_HISTORY_LEN:
            self.channel_history.pop(0)

    @property
    def active_channel(self):
        counter = Counter([t[0] for t in self.channel_history])
        return counter.most_common(1)[0]

    def purge(self):
        if len(self.channel_history) == 0:
            return

        if self.channel_history[0][1] < self.channel_history[-1][1] - 60 * 60 * 2:
            self.channel_history = []
