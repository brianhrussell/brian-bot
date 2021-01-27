from role_utils import BaseRole
from role_utils import CardColor
from role_utils import TeamColor


class RedTeamRole(BaseRole):
    def __init__(self):
        self.name = "Red Team"
        self.directions = "TODO."
        self.color = CardColor.RED
        self.team = TeamColor.RED
        self.max_role_count = 0
        self.allows_buried_role = False
        self.modifiers = list()
        self.required_roles = ['Bomb', 'President']
