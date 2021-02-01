from unittest import mock
import asynctest
from commands.start_game_command import StartGame   # pylint: disable=import-error
import game_tracker                                 # pylint: disable=import-error

sent_messages = list()


class BotCommandTest(asynctest.TestCase):
    def setUp(self):
        _sent_messages = list()

    def tearDown(self):
        print('\n   >>>'.join(sent_messages))
        sent_messages.clear()
        game_tracker.global_tracker.remove_all_games()


async def printSentMessage(msg, channel):
    sent_messages.append(msg)


async def start_game_with_mocks_async(game_name):
    message_mock = mock.Mock(name='message')
    message_mock.guild = 'mock_guild'
    client_mock = mock.Mock(name='client')
    handler = StartGame()
    await handler.handle([game_name], message_mock, client_mock)
    return message_mock, client_mock


class MockDiscordUser(mock.Mock):

    async def add_roles(self, roles):
        self('add', roles)

    async def remove_roles(self, roles):
        self('remove', roles)
