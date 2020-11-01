import json


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

        self.hopped_from = None
        self.hopped_to = None
        self.messages_in_from = None
        self.vader_score = None

    def parse_custom(self):
        obj = self.message_obj

        self.content = obj["content"]
        self.user = obj["user"]

        self.badge_info = obj["badge_info"]
        self.badges = obj["badges"]
        self.color = obj["color"]
        self.display_name = obj["display_name"]
        self.emotes = obj["emotes"]
        self.flags = obj["flags"]
        self.id = obj["id"]
        self.is_mod = obj["is_mod"]
        self.room_id = obj["room_id"]
        self.is_subscriber = obj["is_subscriber"]
        self.tmi_sent_ts = obj["tmi_sent_ts"]
        self.is_turbo = obj["is_turbo"]
        self.user_id = obj["user_id"]
        self.user_type = obj["user_type"]
        self.client_nonce = obj["client_nonce"]
        self.is_emote_only = obj["is_emote_only"]
        self.bits = obj["bits"]
        self.message_id = obj["message_id"]
        self.custom_reward_id = obj["custom_reward_id"]
        self.sent_ts = obj["sent_ts"]

        self.reply_parent_display_name = obj["reply_parent_display_name"]
        self.reply_parent_message_body = obj["reply_parent_message_body"]
        self.reply_parent_message_id = obj["reply_parent_message_id"]
        self.reply_parent_user_id = obj["reply_parent_user_id"]
        self.reply_parent_user_login = obj["reply_parent_user_login"]

        self.channel = obj["channel"]
        self.timestamp = obj["timestamp"]

        self.hopped_from = obj["hopped_from"]
        self.hopped_to = obj["hopped_to"]
        self.messages_in_from = obj["messages_in_from"]
        self.vader_score = obj["vader_score"]

    def parse_twitch(self):
        obj = self.message_obj
        self.content = obj["content"]
        self.user = obj["user"]

        for tag in obj["tags"]:
            key = tag["key"]
            value = tag["value"]
            # print(f"key: {key}, value: {value}")
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

    def to_custom_json(self):
        obj = {
            "content": self.content,
            "user": self.user,
            "badge_info": self.badge_info,
            "badges": self.badges,
            "color": self.color,
            "display_name": self.display_name,
            "emotes": self.emotes,
            "flags": self.flags,
            "id": self.id,
            "is_mod": self.is_mod,
            "room_id": self.room_id,
            "is_subscriber": self.is_subscriber,
            "tmi_sent_ts": self.tmi_sent_ts,
            "is_turbo": self.is_turbo,
            "user_id": self.user_id,
            "user_type": self.user_type,
            "client_nonce": self.client_nonce,
            "bits": self.bits,
            "message_id": self.message_id,
            "custom_reward_id": self.custom_reward_id,
            "sent_ts": self.sent_ts,
            "reply_parent_display_name": self.reply_parent_display_name,
            "reply_parent_message_body": self.reply_parent_message_body,
            "reply_parent_message_id": self.reply_parent_message_id,
            "reply_parent_user_id": self.reply_parent_user_id,
            "reply_parent_user_login": self.reply_parent_user_login,
            "channel": self.channel,
            "timestamp": self.timestamp,
            "hopped_from": self.hopped_from,
            "hopped_to": self.hopped_to,
            "messages_in_from": self.messages_in_from,
            "vader_score": self.vader_score
        }
        return json.dumps(obj)
