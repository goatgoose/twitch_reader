import irc.bot
import requests
import pprint
import time
import json


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, output_dir):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
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
        with open(f"{self.output_dir}/{self.channel[1:]}.json", "a") as out:
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


if __name__ == '__main__':
    bot = TwitchBot("hollowglow", "lfacqb746t1ldb00o1v0j6xnrf8keh", "vs74r4yksospx6ddsac705x1uum785", "pokimane", "data")
    bot.start()
