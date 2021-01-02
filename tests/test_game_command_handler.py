import unittest
from unittest import mock
import asynctest
from commands.game_command import Game
from commands.listgames_command import ListGames
from commands.start_game_command import StartGame

_sent_messages = list()

class TestGameCommandHandler(asynctest.TestCase):
    def setUp(self):
        _sent_messages = list()

    def tearDown(self):
        print('\n'.join(_sent_messages))

    async def test_game_command(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = TestGameCommandHandler._printSentMessage
            handler = Game()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)
    
    async def test_gamelist_command(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = TestGameCommandHandler._printSentMessage
            handler = ListGames()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)

    async def test_startgame_command(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = TestGameCommandHandler._printSentMessage
            handler = StartGame()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)


    @staticmethod
    def _printSentMessage(msg, channel):
        _sent_messages.append('   >>>'+msg)

if __name__ == "__main__":
    unittest.main()
