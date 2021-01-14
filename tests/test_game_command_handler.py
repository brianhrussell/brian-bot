import unittest
from unittest import mock
import asynctest
from commands.game_command import Game              # pylint: disable=import-error
from commands.listgames_command import ListGames    # pylint: disable=import-error
from commands.start_game_command import StartGame   # pylint: disable=import-error
from commands.end_game_command import EndGame       # pylint: disable=import-error
import game_tracker                                 # pylint: disable=import-error
# TODO import these programatically or probably just split these tests into separate files

_sent_messages = list()


class TestGameCommandHandler(asynctest.TestCase):

    def setUp(self):
        _sent_messages = list()

    def tearDown(self):
        print('\n   >>>'.join(_sent_messages))
        _sent_messages.clear()
        game_tracker.global_tracker.remove_all_games()

    async def test_game_command(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = _printSentMessage
            handler = Game()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)

    async def test_gamelist_command(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = _printSentMessage
            handler = ListGames()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)
            self.assertTrue('joinablegame' in _sent_messages[0])
            self.assertTrue('Supported games:' in _sent_messages[0])

    async def test_start_game_command_noargs_error_response(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = _printSentMessage
            handler = StartGame()
            await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
            self.assertEqual(1, mock_send.call_count)
            self.assertTrue('something was wrong with' in _sent_messages[0])

    async def test_startgame_joinablegame_command_constructs_game(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = _printSentMessage
            handler = StartGame()

            await handler.handle(['joinablegame'], mock.Mock(name='message'), mock.Mock(name='client'))

            self.assertEqual(1, mock_send.call_count)
            self.assertTrue('started the game joinablegame' in _sent_messages)
            game_mapping = game_tracker.global_tracker.guild_mapping
            self.assertEqual(1, len(game_mapping))
            game = next(v for k, v in game_mapping.items())
            self.assertTrue(game.__class__.__name__ == 'JoinableGame')

    async def test_joinablegamerunning_joincommand_joinsgame(self):
        with mock.patch('commands.base_command.BaseCommand.send_response') as mock_send:
            mock_send.side_effect = _printSentMessage
            message_mock, client_mock = await _start_game_with_mocks_async()

            game_handler = Game()
            await game_handler.handle(['join'], message_mock, client_mock)

            self.assertEqual(2, mock_send.call_count)
            self.assertTrue('added <Mock' in _sent_messages[1])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_gamerunning_endgamecommand_removes_game(self, send_response_mock):
        send_response_mock.side_effect = _printSentMessage
        message_mock, client_mock = await _start_game_with_mocks_async()

        handler = EndGame()
        await handler.handle(['joinablegame'], message_mock, client_mock)
        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('ended the game joinablegame' in _sent_messages)
        game_mapping = game_tracker.global_tracker.guild_mapping
        self.assertEqual(0, len(game_mapping))


def _printSentMessage(msg, channel):
    _sent_messages.append(msg)


async def _start_game_with_mocks_async():
    message_mock = mock.Mock(name='message')
    message_mock.guild = 'mock_guild'
    client_mock = mock.Mock(name='client')
    handler = StartGame()
    await handler.handle(['joinablegame'], message_mock, client_mock)
    return message_mock, client_mock


if __name__ == "__main__":
    unittest.main()
