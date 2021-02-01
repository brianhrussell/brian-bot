from enum import Enum

from utils import get_emoji


class BaseRole:

    def __init__(self, name, directions, color, team, max_role_count, allows_buried_role, required_roles, modifiers):
        self.name = name
        self.directions = directions
        self.color = color
        self.team = team
        self.max_role_count = max_role_count
        self.allows_buried_role = allows_buried_role
        self.required_roles = required_roles
        self.modifiers = modifiers

    def color_string(self):
        if self.color == CardColor.GREY:
            return get_emoji('white_square')
        if self.color == CardColor.RED:
            return get_emoji('red_square')
        if self.color == CardColor.BLUE:
            return get_emoji('blue_square')

    def team_string(self):
        if self.team == TeamColor.GREY:
            return 'GREY'
        if self.team == TeamColor.RED:
            return 'RED'
        if self.team == TeamColor.BLUE:
            return 'BLUE'

    def to_string(self):
        s = f'''__{self.color_string()} {self.name}__
team: {self.team_string()}
> {self.directions}'''
        return s


class CardColor(Enum):
    GREY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    PURPLE = 4


class TeamColor(Enum):
    GREY = 0
    RED = 1
    BLUE = 2
