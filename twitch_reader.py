import irc.bot
import requests
import pprint
import time
import json
import multiprocessing


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, output_dir):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel.lower()
        self.output_dir = output_dir

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        with open(f"{self.output_dir}/{self.channel[1:]}.json", "a+") as out:
            parsed = self.parse(e)
            json_out = json.dumps(parsed)
            out.write(f"{json_out}\n")
            out.close()

    @staticmethod
    def parse(message):
        return {
            "content": message.arguments[0],
            "user": message.source.split("!")[0],
            "tags": message.tags,
            "channel": message.target[1:],
            "timestamp": time.time()
        }


class BotSpawner:
    def __init__(self, username, client_id, client_secret, token, output_dir, game_id):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.output_dir = output_dir
        self.game_id = game_id

        self.bots = {}  # channel : bot

    def run(self):
        while True:
            channels = self._poll_top_channels()
            for channel in channels:
                if channel not in self.bots:
                    print(f"new channel found: {channel}")
                    process = multiprocessing.Process(target=self._target, args=(channel,))
                    process.start()
                    self.bots[channel] = process

            to_terminate = []
            for channel in self.bots.keys():
                if channel not in channels:
                    to_terminate.append(channel)
            while len(to_terminate) > 0:
                to_remove = to_terminate.pop()
                print(f"removing stale channel: {to_remove}")
                self.bots.pop(to_remove).terminate()

            time.sleep(60 * 20)

    def _poll_top_channels(self):
        token_url = "https://id.twitch.tv/oauth2/token"
        token_request = requests.post(token_url, {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        })
        token = token_request.json()["access_token"]

        url = "https://api.twitch.tv/helix/streams/?game_id=510218&language=en&first=5"
        headers = {
            'client-id': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f"Bearer {token}"
        }
        streams = {stream["user_name"] for stream in requests.get(url, headers=headers).json()["data"]}
        return streams

    def _target(self, channel):
        bot = TwitchBot(self.username, self.client_id, self.token, channel, self.output_dir)
        bot.start()


if __name__ == '__main__':
    spawner = BotSpawner(
        "hollowglow",
        "lfacqb746t1ldb00o1v0j6xnrf8keh",
        "6gcjxjdznyukse5vv3qm1a49djw24p",
        "vs74r4yksospx6ddsac705x1uum785",
        "data",
        510218
    )
    spawner.run()
