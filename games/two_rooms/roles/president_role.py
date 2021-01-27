from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles.role_utils import CardColor
from games.two_rooms.roles.role_utils import TeamColor


class PresidentRole(BaseRole):
    def __init__(self):
        self.name = "President"
        self.directions = "TODO."
        self.color = CardColor.BLUE
        self.team = TeamColor.BLUE
        self.max_role_count = 1
        self.allows_buried_role = False
        self.modifiers = list()
        self.required_roles = ['Bomb']
