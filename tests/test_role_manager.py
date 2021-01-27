from games.two_rooms.players import RoleManager

import unittest
from unittest import mock


class TwoRoomsRoleManagerTest(unittest.TestCase):

    def test_available_roles_finds_roles(self):
        manager = RoleManager()
        self.assertEqual(len(manager.role_factory), 4)


if __name__ == "__main__":
    unittest.main()
