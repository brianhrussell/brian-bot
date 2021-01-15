import unittest
from unittest import mock
import asynctest

import test_helpers
from commands.game_command import Game              # pylint: disable=import-error
from commands.listgames_command import ListGames    # pylint: disable=import-error
from commands.start_game_command import StartGame   # pylint: disable=import-error
from commands.end_game_command import EndGame       # pylint: disable=import-error
import game_tracker                                 # pylint: disable=import-error
# TODO import these programatically or probably just split these tests into separate files


class BasicGameCommandTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_game_command(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        handler = Game()
        await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
        self.assertEqual(1, send_response_mock.call_count)

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_joinablegamerunning_joincommand_joinsgame(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('joinablegame')

        game_handler = Game()
        await game_handler.handle(['join'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added <Mock' in test_helpers.sent_messages[1])


class ListGamesCommandTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_gamelist_command(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        handler = ListGames()
        await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
        self.assertEqual(1, send_response_mock.call_count)
        self.assertTrue('joinablegame' in test_helpers.sent_messages[0])
        self.assertTrue('tworooms' in test_helpers.sent_messages[0])
        self.assertTrue('Supported games:' in test_helpers.sent_messages[0])


class StartGameCommandTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_start_game_command_noargs_error_response(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        handler = StartGame()
        await handler.handle([], mock.Mock(name='message'), mock.Mock(name='client'))
        self.assertEqual(1, send_response_mock.call_count)
        self.assertTrue('something was wrong with' in test_helpers.sent_messages[0])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_startgame_joinablegame_command_constructs_game(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        handler = StartGame()

        await handler.handle(['joinablegame'], mock.Mock(name='message'), mock.Mock(name='client'))

        self.assertEqual(1, send_response_mock.call_count)
        self.assertTrue('started the game joinablegame' in test_helpers.sent_messages)
        game_mapping = game_tracker.global_tracker.guild_mapping
        self.assertEqual(1, len(game_mapping))
        game = next(v for k, v in game_mapping.items())
        self.assertTrue(game.__class__.__name__ == 'JoinableGame')


class EndGameCommandTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_gamerunning_endgamecommand_removes_game(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('joinablegame')

        handler = EndGame()
        await handler.handle(['joinablegame'], message_mock, client_mock)
        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('ended the game joinablegame' in test_helpers.sent_messages)
        game_mapping = game_tracker.global_tracker.guild_mapping
        self.assertEqual(0, len(game_mapping))


if __name__ == "__main__":
    unittest.main()
