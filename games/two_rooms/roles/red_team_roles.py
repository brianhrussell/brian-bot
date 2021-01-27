from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles.role_utils import CardColor
from games.two_rooms.roles.role_utils import TeamColor


class RedTeamRole(BaseRole):
    def __init__(self):
        super().__init__(
            name='Red Team',
            directions="TODO.",
            color=CardColor.RED,
            team=TeamColor.RED,
            max_role_count=0,
            allows_buried_role=False,
            required_roles=['Bomb', 'President'],
            modifiers=list())


class BombRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Bomb",
            directions="TODO.",
            color=CardColor.RED,
            team=TeamColor.RED,
            max_role_count=1,
            allows_buried_role=False,
            required_roles=['President'],
            modifiers=list())


class RedSpyRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Red Spy",
            directions="TODO.",
            color=CardColor.BLUE,
            team=TeamColor.RED,
            max_role_count=0,
            modifiers=list(),
            required_roles=['Bomb', 'President'],
            allows_buried_role=False)
