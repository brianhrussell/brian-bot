import unittest
from unittest import mock

from games.two_rooms.role_tracker import RoleTracker


class TwoRoomsRoleTrackerTest(unittest.TestCase):

    def test_available_roles_finds_roles(self):
        tracker = RoleTracker()
        self.assertEqual(len(tracker.role_factory), 6)

    def test_trackerwithfourroles_fourplayersisvalid(self):
        tracker = RoleTracker()
        tracker.add_role('president')
        tracker.add_role('bomb')
        tracker.add_role('redteam')
        tracker.add_role('blueteam')
        self.assertTrue(tracker.roles_are_valid(4))

    def test_trackerwithfourroles_fiveplayersisnotvalid(self):
        tracker = RoleTracker()
        tracker.add_role('president')
        tracker.add_role('bomb')
        tracker.add_role('redteam')
        tracker.add_role('blueteam')
        self.assertFalse(tracker.roles_are_valid(5))

    def test_trackerwithmissingrequiredrole_setisnotvalid(self):
        tracker = RoleTracker()
        tracker.add_role('president')
        tracker.add_role('redteam')
        tracker.add_role('redteam')
        tracker.add_role('blueteam')

        self.assertFalse(tracker.roles_are_valid(4))

    def test_trackerwithfourroles_dealroles(self):
        tracker = RoleTracker()
        roles = ['president', 'bomb', 'redteam', 'blueteam']
        self.add_roles(tracker, roles)

        num_players = len(roles)
        player_mocks = self.deal_roles(tracker, num_players)

        self.assertEqual(0, len(tracker.unassigned_roles))
        for role in roles:
            self.assert_num_players_with_role(1, tracker.role_factory[role], player_mocks)

    def deal_roles(self, tracker, num_players):
        player_mocks = list()
        for i in range(0, num_players):  # pylint: disable=unused-variable
            user_mock = mock.Mock()
            player_mocks.append(tracker.deal_role(user_mock))
        return player_mocks

    def add_roles(self, tracker, role_names):
        for role in role_names:
            tracker.add_role(role)

    def assert_num_players_with_role(self, n, role_class, players):
        self.assertEqual(n, sum(1 for m in players if m.role.__class__ is role_class))


if __name__ == "__main__":
    unittest.main()
