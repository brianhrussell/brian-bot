from games.two_rooms.role_tracker import RoleTracker

import unittest
from unittest import mock


class TwoRoomsRoleTrackerTest(unittest.TestCase):

    def test_available_roles_finds_roles(self):
        manager = RoleTracker()
        self.assertEqual(len(manager.role_factory), 6)


if __name__ == "__main__":
    unittest.main()
