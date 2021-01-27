from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles.role_utils import CardColor
from games.two_rooms.roles.role_utils import TeamColor


class BombRole(BaseRole):
    def __init__(self):
        self.name = "Bomb"
        self.directions = "TODO."
        self.color = CardColor.RED
        self.team = TeamColor.RED
        self.max_role_count = 1
        self.allows_buried_role = False
        self.modifiers = list()
        self.required_roles = ['President']
