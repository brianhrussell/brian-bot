import unittest
from unittest import mock
import asynctest
import settings
import discord
import game_bot
import message_handler

class Test_Bot(asynctest.TestCase):

    async def test_the_test(self):
        await _send_string('!game')
        self.assertEqual(1,1)


# static helpers
async def _send_string(text):
        mockmessage = mock.Mock(name='message')
        mockclient = mock.Mock(name='client')
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(cmd_split[0].lower(), 
                                        cmd_split[1:], mockmessage, mockclient)
            except:
                print("Error while handling message", flush=True)
                raise

if __name__ == "__main__":
    unittest.main()