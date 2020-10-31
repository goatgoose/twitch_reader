
class ChatMessage:
    def __init__(self, message_obj):
        self.message_obj = message_obj

        self.content = None
        self.user = None

        self.badge_info = None
        self.badges = None
        self.color = None
        self.display_name = None
        self.emotes = None
        self.flags = None
        self.id = None
        self.is_mod = None
        self.room_id = None
        self.is_subscriber = None
        self.tmi_sent_ts = None
        self.is_turbo = None
        self.user_id = None
        self.user_type = None
        self.client_nonce = None
        self.is_emote_only = None
        self.bits = None
        self.message_id = None
        self.custom_reward_id = None
        self.sent_ts = None

        self.reply_parent_display_name = None
        self.reply_parent_message_body = None
        self.reply_parent_message_id = None
        self.reply_parent_user_id = None
        self.reply_parent_user_login = None

        self.channel = None
        self.timestamp = None

        self.parse(self.message_obj)

    def parse(self, obj):
        self.content = obj["content"]
        self.user = obj["user"]

        for tag in obj["tags"]:
            key = tag["key"]
            value = tag["value"]
            print(f"key: {key}, value: {value}")
            {
                "badge-info": lambda: setattr(self, "badge_info", value),
                "badges": lambda: setattr(self, "badges", value.split(",") if value else []),
                "color": lambda: setattr(self, "color", value),
                "display-name": lambda: setattr(self, "display_name", value),
                "emotes": lambda: setattr(self, "emotes", value),
                "flags": lambda: setattr(self, "flags", value if value else []),
                "id": lambda: setattr(self, "id", value),
                "mod": lambda: setattr(self, "is_mod", bool(int(value))),
                "room-id": lambda: setattr(self, "room_id", value),
                "subscriber": lambda: setattr(self, "is_subscriber", bool(int(value))),
                "tmi-sent-ts": lambda: setattr(self, "tmi_sent_is", value),
                "turbo": lambda: setattr(self, "is_turbo", bool(int(value))),
                "user-id": lambda: setattr(self, "user_id", value),
                "user-type": lambda: setattr(self, "user_type", value),
                "client-nonce": lambda: setattr(self, "client_nonce", value),
                "emote-only": lambda: setattr(self, "is_emote_only", value),
                "bits": lambda: setattr(self, "bits", value),
                "msg-id": lambda: setattr(self, "message_id", value),
                "custom-reward-id": lambda: setattr(self, "custom_reward_id", value),
                "reply-parent-display-name": lambda: setattr(self, "reply_parent_display_name", value),
                "reply-parent-msg-body": lambda: setattr(self, "reply_parent_message_body", value),
                "reply-parent-msg-id": lambda: setattr(self, "reply_parent_message_id", value),
                "reply-parent-user-id": lambda: setattr(self, "reply_parent_user_id", value),
                "reply-parent-user-login": lambda: setattr(self, "reply_parent_user_login", value),
                "sent-ts": lambda: setattr(self, "sent_ts", value)
            }.get(key)()

        self.channel = obj["channel"]
        self.timestamp = obj["timestamp"]
