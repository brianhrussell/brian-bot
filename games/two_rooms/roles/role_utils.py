from enum import Enum
from utils import get_emoji


class BaseRole:

    def __init__(self):
        self.color = CardColor.GREY
        self.team = TeamColor.GREY
        self.max_role_count = 0
        self.allows_buried_role = False
        self.name = "Base Role"
        self.directions = "This role shouldn't show up in the list."
        self.modifiers = list()
        self.required_roles = ['Bomb', 'President']

# can probably do this programatically but probably not worth bothering
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
