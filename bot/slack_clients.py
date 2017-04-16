
import logging
import re
import time

from slacker import Slacker
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']

    def is_message_from_me(self, user):
        return user == self.rtm.server.login_data['self']['id']

    def is_bot_mention(self, message):
        bot_user_name = self.rtm.server.login_data['self']['id']
        if re.search("@{}".format(bot_user_name), message):
            return True
        else:
            return False

    def send_user_typing_pause(self, channel_id, sleep_time=3.0):
        user_typing_json = {"type": "typing", "channel": channel_id}
        self.rtm.server.send_to_websocket(user_typing_json)
        time.sleep(sleep_time)

    def is_message_from_emma(self, user_id):
        x = self.web.users.list()
        for user in x.body["members"]:
            if user["id"] == user_id and user["name"] == "emma":
                return True
        return False

    def is_message_from_taylor(self, user_id):
        x = self.web.users.list()
        for user in x.body["members"]:
            if user["id"] == user_id and user["name"] == "taylor":
                return True
        return False

    def is_message_from_parker(self, user_id):
        x = self.web.users.list()
        for user in x.body["members"]:
            if user["id"] == user_id and user["name"] == "parker":
                return True
        return False
