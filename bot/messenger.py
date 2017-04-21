# -*- coding: utf-8 -*-

import logging
import random
import json

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.schedule = "no schedule right now"
        self.commitments = dict()
        self.remaining = []

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id, user_id):
        if self.clients.is_message_from_parker(user_id):
            txt = "Why are you bothering me? Go play Persona or something."
            self.send_message(channel_id, txt)
        else:
            bot_uid = self.clients.bot_user_id()
            txt = self.get_help_message(bot_uid)
            self.send_message(channel_id, txt)

    def get_help_message(self, bot_uid):
        txt = '{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm a somewhat friendly, somewhat sassy slackbot.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user :wave:",
            "> `<@" + bot_uid + "> what's left?` - I'll let you know what you have to do before this project is over",
            "> `<@" + bot_uid + "> update what's left with <item>` - I'll add something to the list of what's left to do",
            "> `<@" + bot_uid + "> remove <numbered item> from what's left` - I'll remove the numbered item from the list of what's left to do",
            "> `<@" + bot_uid + "> bye` - I'll bid you a sorrowful farewell :cry:",
            "> `<@" + bot_uid + "> schedule` - I'll respond with your schedule for the week.")
        return txt

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Salutations', 'Greetings human']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    # def demo_attachment(self, channel_id):
    #     txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
    #     attachment = {
    #         "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
    #         "title": "Host, deploy and share your bot in seconds.",
    #         "title_link": "https://beepboophq.com/",
    #         "text": txt,
    #         "fallback": txt,
    #         "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
    #         "color": "#7CD197",
    #     }
    #     self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def update_schedule(self, msg_txt):
        self.schedule = msg_txt

    def write_schedule(self, channel_id):
        txt = self.schedule
        self.send_message(channel_id, txt)

    def upate_commitments(self, channel_id, user_id, msg_txt):
        self.commitments[user_id] = msg_txt

    def write_commitments(self, channel_id, user_id):
        txt = "Your stand-up message today: " + self.commitments[user_id]
        self.send_message(channel_id, txt)

    def write_amf(self, channel_id, user_id):
        txt_emma = ["AMF :heart: I love you team lead!!!", "#AMF", "AndrewsMontrossForever", ":heart_eyes: :heart_eyes: :heart_eyes:", "YOU. ARE. AMAZING. #AMF"]
        txt_taylor = ["#AMFAMFAMFAMFAMF", "#AMF", "Babe, our house will be amazing! #AMF", "Thai food soon? #AMF"]
        if self.clients.is_message_from_emma(user_id):
            self.send_message(channel_id, random.choice(txt_emma))
        elif self.clients.is_message_from_taylor(user_id):
            self.send_message(channel_id, random.choice(txt_taylor))

    def write_goodbye(self, channel_id):
        farewell = ["Your departure maketh me cry a river", "I have never loved like I love you, human", "Verily, this goodbye must be what death feels like",
                    "...bye :sob:", "I want you to know I will always remember you", "I hope we meet again in the robot afterlife. Wait did I just expose you as a fellow robot? My bad.",
                    "Wasn't feeling this conversation anyway."]
        self.send_message(channel_id, random.choice(farewell))

    def write_remaining(self, channel_id):
        if len(self.remaining) > 0:
            i = 1
            txt = "Here's what's left:\n"
            for remaining_item in self.remaining:
                txt += "\t{0}. {1}\n".format(i, remaining_item)
                i += 1
            self.send_message(channel_id, txt)
        else:
            self.send_message(channel_id, "Hey, there's nothing left for you to do. I guess you finished the project!")

    def update_remaining(self, channel_id, user, txt):
        self.remaining.append(txt)
        self.send_message(channel_id, "Okay <@{0}>, '{1}' was added".format(user, txt.strip()))

    def remove_remaining(self, channel_id, numbers_to_remove):
        max_num = len(self.remaining)
        for i in sorted(numbers_to_remove, reverse=True):
            if i <= max_num:
                del self.remaining[i-1]

        self.send_message(channel_id, "Removed!")

    def write_language_sass(self, channel_id):
        txt = ["I don't appreciate your language. Go wash your mouth out and then I can help you.", "That kind of language hurts my feelings.", ":middle_finger:",
               "Do not speak to me that way, young lady."]
        self.send_message(channel_id, random.choice(txt))