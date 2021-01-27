from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles import *  # pylint: disable=unused-wildcard-import

# Register all available roles
ROLE_FACTORY = {c.__name__.lower(): c
                for c in BaseRole.__subclasses__()}


class Player:
    def __init__(self, discord_user, role):
        self.user = discord_user
        self.role = role


class RoleManager:
    def __init__(self):
        self.role_factory = ROLE_FACTORY
        self.unassigned_roles = list()
        self.players = list()
