from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles import *

# Register all available roles
AVAILABLE_ROLES = {c.__name__.lower(): c()
                   for c in BaseRole.__subclasses__()}


class Player:
    def __init__(self, discord_user, role):
        self.user = discord_user
        self.role = role


class RoleManager:
    def __init__(self):
        self.available_roles = AVAILABLE_ROLES
        self.unassigned_roles = list()
        self.players = list()
