import unittest
from unittest import mock
import asynctest

import test_helpers
from commands.game_command import Game              # pylint: disable=import-error
from commands.start_game_command import StartGame   # pylint: disable=import-error


class TwoRoomsGameTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_joinablegamerunning_joincommand_joinsgame(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['join'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added <Mock' in test_helpers.sent_messages[1])

# TODO don't duplicate these move them into a test helpers file


if __name__ == "__main__":
    unittest.main()
