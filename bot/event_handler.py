import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.stand_up = self.get_standup_channel_id()

    def get_standup_channel_id(self):
        return self.clients.web.channels.get_channel_id('stand-up')

    def get_bottest_channel_id(self):
        return self.clients.web.channels.get_channel_id('testing-bots')

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            msg_txt = event['text']

            if self.clients.is_bot_mention(msg_txt) or self._is_direct_message(event['channel']):
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'], event['user'])
                elif re.search('hi|hey|hello', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                elif 'schedule' in msg_txt:
                    self.msg_writer.write_schedule(event['channel'])
                elif 'stand-up' in msg_txt or 'commit' in msg_txt:
                    if 'taylor' in msg_txt or 'Taylor' in msg_txt:
                        self.msg_writer.write_commitments(event['channel'], self.clients.get_user_id("taylor"), "Taylor's")
                    if 'pete' in msg_txt or 'Pete' in msg_txt:
                        self.msg_writer.write_commitments(event['channel'], self.clients.get_user_id("pete_m"), "Pete's")
                    if 'emma' in msg_txt or 'Emma' in msg_txt:
                        self.msg_writer.write_commitments(event['channel'], self.clients.get_user_id("emma"), "Emma's")
                    if 'ben' in msg_txt or 'Ben' in msg_txt:
                        self.msg_writer.write_commitments(event['channel'], self.clients.get_user_id("bendroste"), "Ben's")
                    if 'parker' in msg_txt or 'Parker' in msg_txt:
                        self.msg_writer.write_commitments(event['channel'], self.clients.get_user_id("parker"), "Parker's")
                    if not re.search('[Tt]aylor|[Ee]mma|[Bb]en|[Pp]arker|[Pp]ete', msg_txt):
                        self.msg_writer.write_commitments(event['channel'], event['user'])
                elif "what's left" in msg_txt or 'graduate' in msg_txt:
                    if 'update' in msg_txt:
                        self.msg_writer.update_remaining(event['channel'], event['user'], msg_txt.split("with")[-1])
                    elif "remove" in msg_txt:
                        self.msg_writer.remove_remaining(event['channel'], [int(s) for s in msg_txt.split() if s.isdigit()])
                    else:
                        self.msg_writer.write_remaining(event['channel'])
                elif 'AMF' in msg_txt or 'amf' in msg_txt:
                    self.msg_writer.write_amf(event['channel'], event['user'])
                elif re.search('bye|farewell|peace|goodbye', msg_txt):
                    self.msg_writer.write_goodbye(event['channel'])
                else:
                    self.msg_writer.write_prompt(event['channel'])

            elif event['channel'] == self.stand_up:
                self.msg_writer.update_commitments(event['user'], msg_txt)

            elif event['channel'] == self.get_bottest_channel_id():
                self.msg_writer.update_commitments(event['user'], msg_txt)

        elif 'user' not in event and self._is_direct_message(event['channel']):
            msg_txt = event['text']
            self.msg_writer.update_schedule(msg_txt)


    def _is_direct_message(self, channel):
        """Check if channel is a direct message channel

        Args:
            channel (str): Channel in which a message was received
        """
        return channel.startswith('D')
