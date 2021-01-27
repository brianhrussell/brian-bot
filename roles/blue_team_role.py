from role_utils import BaseRole
from role_utils import CardColor
from role_utils import TeamColor


class BlueTeamRole(BaseRole):
    def __init__(self):
        self.name = "Blue Team"
        self.directions = "TODO."
        self.color = CardColor.BLUE
        self.team = TeamColor.BLUE
        self.max_role_count = 0
        self.modifiers = list()
        self.required_roles = ['Bomb', 'President']
        self.allows_buried_role = False
