from games.two_rooms.role_tracker import RoleTracker

import unittest
from unittest import mock


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


if __name__ == "__main__":
    unittest.main()
