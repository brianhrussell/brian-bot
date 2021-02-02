import unittest
from unittest import mock
from unittest.mock import Mock

import asynctest

import test_helpers
from commands.game_command import G  # pylint: disable=import-error
from game_tracker import get_game_for_guild
from games.two_rooms_game import TwoRooms
from games.two_rooms_game import TwoRoomsState
from games.two_rooms.player import Player


class TwoRoomsGameTests(test_helpers.BotCommandTest):

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworooms_game_running_joincommand_joinsgame(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
        await game_handler.handle(['join'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added <Mock' in test_helpers.sent_messages[1])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_addrolecommandnoparam_doesntaddrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
        await game_handler.handle(['add-role'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('provide a role name' in test_helpers.sent_messages[1])
        two_rooms_game = get_game_for_guild('mock_guild')
        self.assertEqual(0, len(two_rooms_game.role_tracker.unassigned_roles))

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamerunning_addrolecommand_addsrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('added roles successfully' in test_helpers.sent_messages[1])
        two_rooms_game = get_game_for_guild('mock_guild')
        self.assertEqual(1, len(two_rooms_game.role_tracker.unassigned_roles))
        self.assertEqual(two_rooms_game.role_tracker.unassigned_roles[0].name, 'Bomb')

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithonerole_removerolecommand_removesrole(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
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

        game_handler = G()
        await game_handler.handle(['list-roles'], message_mock, client_mock)

        self.assertEqual(2, send_response_mock.call_count)
        self.assertTrue('President' in test_helpers.sent_messages[1])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithtworoles_getselected_rolesarelisted(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)
        await game_handler.handle(['add-role', 'President'], message_mock, client_mock)
        await game_handler.handle(['selected-roles'], message_mock, client_mock)

        self.assertEqual(4, send_response_mock.call_count)
        self.assertTrue('selected roles:\nPresident x1\nBomb x1' in test_helpers.sent_messages[3])

    @mock.patch('commands.base_command.BaseCommand.send_response')
    async def test_tworoomsgamewithtworoles_begingame_rolesarenotvalid(self, send_response_mock):
        send_response_mock.side_effect = test_helpers.printSentMessage
        message_mock, client_mock = await test_helpers.start_game_with_mocks_async('tworooms')

        game_handler = G()
        await game_handler.handle(['add-role', 'Bomb'], message_mock, client_mock)
        await game_handler.handle(['add-role', 'President'], message_mock, client_mock)
        await game_handler.handle(['begin'], message_mock, client_mock)

        self.assertEqual(4, send_response_mock.call_count)
        self.assertTrue('you need more people to play' in test_helpers.sent_messages[3])


class RoomTests(asynctest.TestCase):
    async def test_assign_players_to_rooms(self):
        for case in [2, 4, 7, 10, 31]:
            tworooms = TwoRooms(Mock(), Mock())
            tworooms.players = await self.generate_players_dict(case)
            await tworooms.assign_rooms()
            self.assertTrue(self.rooms_are_valid(tworooms))

    async def test_assign_leaders_randomly(self):
        for case in [2, 4, 7, 10, 31]:
            tworooms = TwoRooms(Mock(), Mock())
            tworooms.players = await self.generate_players_dict(case)
            await tworooms.assign_rooms()
            tworooms.assign_leaders_randomly()
            self.assertTrue(self.rooms_are_valid(tworooms))
            self.assertTrue(tworooms.rooms[0].leader in tworooms.rooms[0].players)
            self.assertTrue(tworooms.rooms[1].leader in tworooms.rooms[1].players)

    @mock.patch('games.two_rooms.room.Room.send_message')
    async def test_round_start_event(self, send_response_mock):
        tworooms = await self.create_test_tworooms_game(12)

        await tworooms.events.fire('on_round_start', 1)
        self.assertEqual(2, send_response_mock.call_count)

        first_message = self.get_mock_send_parameter(send_response_mock, 0)
        second_message = self.get_mock_send_parameter(send_response_mock, 1)
        self.assertTrue('start of round 1' in first_message and 'start of round 1' in second_message)
        self.assertNotEqual(first_message, second_message)

    async def test_set_sent_hostage_invalid(self):
        tworooms = await self.create_test_tworooms_game(10)
        msg = await self.set_sent_hostages(tworooms, 0, 2)
        self.assertTrue('invalid' in msg)

    async def test_set_sent_hostage_valid(self):
        tworooms = await self.create_test_tworooms_game(10)
        msg = await self.set_sent_hostages(tworooms, 0, 1)
        self.assertFalse('invalid' in msg)

    async def test_exchange_hostages(self):
        tworooms = await self.create_test_tworooms_game(10)
        room1 = tworooms.rooms[1]
        room0 = tworooms.rooms[0]
        await self.set_sent_hostages(tworooms, 0, 1)
        await self.set_sent_hostages(tworooms, 1, 1)
        original_rooms = [room0.players.copy(), room1.players.copy()]
        sent_hostages = [room0.next_sent_hostages.copy(), room1.next_sent_hostages.copy()]
        await tworooms.exchange_hostages()
        self.assertEqual(room0.channel.call_count, 1)
        self.assertEqual(room1.channel.call_count, 1)
        await self.assert_players_were_transferred(tworooms, sent_hostages, original_rooms)

    async def assert_players_were_transferred(self, tworooms, sent_hostages, original_rooms):
        for room_number in range(2):
            players_are_still_in_room = any(
                True for player in sent_hostages[room_number] if player.user in tworooms.rooms[room_number].players)
            players_were_originally_in_room = all(
                True for player in sent_hostages[room_number] if player.user in original_rooms)
            self.assertFalse(players_are_still_in_room)
            self.assertTrue(players_were_originally_in_room)

    async def test_end_game_message(self):
        tworooms = await self.create_test_tworooms_game(10)
        tworooms.round = 4
        channel_mock = Mock()
        tworooms.start_channel = channel_mock
        await tworooms.on_round_start_event(4)
        self.assertTrue(channel_mock.send.call_count > 0)
        self.assertTrue('game has finished' in self.get_mock_send_parameter(channel_mock, 0))

    @staticmethod
    async def create_test_tworooms_game(num_players):
        tworooms = TwoRooms(Mock(), Mock())
        tworooms.players = await RoomTests.generate_players_dict(num_players)
        await tworooms.assign_rooms()
        tworooms.rooms[0].channel = test_helpers.MockDiscordChannel()
        tworooms.rooms[1].channel = test_helpers.MockDiscordChannel()
        tworooms.assign_leaders_randomly()
        tworooms.state = TwoRoomsState.PLAYING
        tworooms.round = 1
        return tworooms

    @staticmethod
    def get_mock_send_parameter(send_response_mock, call_number):
        return send_response_mock.mock_calls[call_number][1][0]

    @staticmethod
    async def generate_players_dict(num_players):
        players = dict()
        for i in range(num_players):
            player = Player(test_helpers.MockDiscordUser())
            mock_role = Mock(name='role')
            mock_role.to_string = Mock(return_value="mock_role.to_string")
            player.user.mention = f'@{i}'
            player.user.dm_channel = test_helpers.MockDiscordChannel(name='dm_channel')
            await player.set_role(mock_role)
            players[player.user] = player
        return players

    @staticmethod
    def rooms_are_valid(tworooms):
        for player in tworooms.players.values():
            return (player in tworooms.rooms[0].players) ^ (player in tworooms.rooms[1].players)

    @staticmethod
    async def set_sent_hostages(tworooms, room_number, num_hostages):
        message_mock = Mock()
        client_mock = Mock()
        message_mock.author = tworooms.rooms[room_number].leader.user
        message_mock.mentions = list(RoomTests.get_non_leader_players(num_hostages, tworooms.rooms[room_number]))
        return await tworooms.set_sent_hostage([], message_mock, client_mock)

    @staticmethod
    def get_non_leader_players(num_players, room):
        room_leader = room.leader
        players = room.players
        i = 0
        for player in players:
            if player is not room_leader:
                i += 1
                yield player.user
            if i >= num_players:
                break


if __name__ == "__main__":
    unittest.main()
