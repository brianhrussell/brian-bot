import unittest
from unittest import mock
import asynctest

import test_helpers
from commands.game_command import Game              # pylint: disable=import-error
from commands.start_game_command import StartGame   # pylint: disable=import-error
from game_tracker import get_game_for_guild
from games.two_rooms_game import TwoRooms


class TwoRoomsGameTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_joincommand_joinsgame(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['join'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added <Mock' in test_helpers.sent_messages[1])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_addrolecommandnoparam_doesntaddrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['add-role'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('provide a role name' in test_helpers.sent_messages[1])
        two_rooms_game = get_game_for_guild('mock_guild')
        self.assertEqual(0, len(two_rooms_game.role_tracker.unassigned_roles))

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_addrolecommand_addsrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added roles successfully' in test_helpers.sent_messages[1])
        two_rooms_game = get_game_for_guild('mock_guild')
        self.assertEqual(1, len(two_rooms_game.role_tracker.unassigned_roles))
        two_rooms_game.role_tracker.unassigned_roles[0].name == 'Bomb'

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithonerole_removerolecommand_removesrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)
        await game_handler.handle(['remove-role', 'Bomb'], message_mock, client_mock)

        self.assertEqual(3, send_response_mock.call_count)
        self.assertTrue('removed roles successfully' in test_helpers.sent_messages[2])
        two_rooms_game = get_game_for_guild('mock_guild')
        self.assertEqual(0, len(two_rooms_game.role_tracker.unassigned_roles))

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_listrolescommand_listsroles(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['list-roles'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('President' in test_helpers.sent_messages[1])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithtworoles_getselected_rolesarelisted(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)
        await game_handler.handle(['add-role', 'President'], message_mock, client_mock)
        await game_handler.handle(['selected-roles'], message_mock, client_mock)

        self.assertEqual(4, send_response_mock.call_count)
        self.assertTrue('selected roles:\npresident x1\nbomb x1' in test_helpers.sent_messages[3])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithtworoles_begingame_rolesarenotvalid(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = Game()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)
        await game_handler.handle(['add-role', 'President'], message_mock, client_mock)
        await game_handler.handle(['begin'], message_mock, client_mock)

        self.assertEqual(4, send_response_mock.call_count)
        self.assertTrue('you need more people to play' in test_helpers.sent_messages[3])


class RoomTests(unittest.TestCase):
    def test_assign_players_to_rooms(self):
        for case in [2, 4, 7, 11, 31]:
            tworooms = TwoRooms(mock.Mock(), mock.Mock())
            tworooms.players = self.generate_room_with_players(case)
            tworooms.assign_rooms()
            self.assert_rooms_are_valid(tworooms)

    @staticmethod
    def generate_room_with_players(num_players):
        d = dict()
        for i in range(num_players):
            d[i] = i
        return d

    def assert_rooms_are_valid(self, tworooms):
        for player in tworooms.players.values():
            self.assertTrue((player in tworooms.rooms[0].players) ^ (player in tworooms.rooms[1].players))


if __name__ == "__main__":
    unittest.main()
