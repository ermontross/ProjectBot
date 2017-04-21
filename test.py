from messenger import get_help_message
import unittest

class TestMessenger(unittest.TestCase):
    def test_text_match(self):
        bot_uid = 1
        expected = '{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm a somewhat friendly, somewhat sassy slackbot.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user :wave:",
            "> `<@" + bot_uid + "> what's left?` - I'll let you know what you have to do before this project is over",
            "> `<@" + bot_uid + "> update what's left with <item>` - I'll add something to the list of what's left to do",
            "> `<@" + bot_uid + "> remove <numbered item> from what's left` - I'll remove the numbered item from the list of what's left to do",
            "> `<@" + bot_uid + "> bye` - I'll bid you a sorrowful farewell :cry:",
            "> `<@" + bot_uid + "> schedule` - I'll respond with your schedule for the week.")
        self.assertEqual(expected, get_help_message(bot_uid))

if __name__ == "__main__":
    unittest.main()