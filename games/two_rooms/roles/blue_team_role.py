from games.two_rooms.roles.role_utils import BaseRole, CardColor, TeamColor


class TestRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Test Role",
            directions="TODO.",
            color=CardColor.BLUE,
            team=TeamColor.BLUE,
            max_role_count=0,
            modifiers=list(),
            required_roles=[],
            allows_buried_role=False)


class BlueTeamRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Blue Team",
            directions="TODO.",
            color=CardColor.BLUE,
            team=TeamColor.BLUE,
            max_role_count=0,
            modifiers=list(),
            required_roles=['Bomb', 'President'],
            allows_buried_role=False)


class PresidentRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="President",
            directions="TODO.",
            color=CardColor.BLUE,
            team=TeamColor.BLUE,
            max_role_count=1,
            allows_buried_role=False,
            modifiers=list(),
            required_roles=['Bomb'])


class BlueSpyRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Blue Spy",
            directions="TODO.",
            color=CardColor.RED,
            team=TeamColor.BLUE,
            max_role_count=0,
            modifiers=list(),
            required_roles=['Bomb', 'President'],
            allows_buried_role=False)
