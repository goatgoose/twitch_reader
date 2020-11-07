
class ChatBlock:
    def __init__(self, channel, duration):
        self.channel = channel
        self.duration = duration  # seconds

        self.start_timestamp = None
        self.last_timestamp = None

        self.message_count = 0
        self.mod_message_count = 0
        self.sub_message_count = 0
        self.turbo_message_count = 0
        self.self_toxic_count = 0
        self.self_positive_count = 0
        self.hopped_toxic_count = 0
        self.hopped_positive_count = 0

    def log_message(self, message):
        if self.start_timestamp is None:
            self.start_timestamp = message.timestamp
        self.last_timestamp = message.timestamp

        self.message_count += 1
        if message.is_mod:
            self.mod_message_count += 1
        if message.is_subscriber:
            self.sub_message_count += 1
        if message.is_turbo:
            self.turbo_message_count += 1

        if message.hopped_from:
            if message.vader_score < -0.42:
                self.hopped_toxic_count += 1
            elif message.vader_score > 0.42:
                self.hopped_positive_count += 1
        else:
            if message.vader_score < -0.42:
                self.self_toxic_count += 1
            elif message.vader_score > 0.42:
                self.self_positive_count += 1

    def will_expire(self, timestamp):
        return timestamp > self.start_timestamp + self.duration

    def _extrapolate_features(self, features):
        time_used = self.last_timestamp - self.start_timestamp
        percent_remaining = self.duration / time_used

        extrapolated = []
        for feature in features:
            extrapolate = feature * (percent_remaining)
            extrapolated.append(extrapolate)
        return extrapolated

    def feature_vec(self):
        extrapolated = self._extrapolate_features([
            self.message_count,
            self.mod_message_count,
            self.sub_message_count,
            self.turbo_message_count,
            self.self_toxic_count,
            self.hopped_toxic_count
        ])
        return [
            self.channel,
            self.duration,
            self.start_timestamp
        ] + extrapolated


if __name__ == '__main__':
    from chat_message import ChatMessage

    chat_block = ChatBlock("test", 100)

    for i in range(90):
        message = ChatMessage({})
        message.timestamp = i
        message.vader_score = 0
        chat_block.log_message(message)
    message = ChatMessage({})
    message.timestamp = 90
    message.vader_score = 0
    message.is_mod = True
    chat_block.log_message(message)

    print(chat_block.feature_vec())


