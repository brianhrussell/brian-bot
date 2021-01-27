from enum import Enum


class BaseRole:

    def __init__(self):
        self.color = CardColor.GREY
        self.team = TeamColor.GREY
        self.max_role_count = 0
        self.allows_buried_role = False
        self.name = "Base Role"
        self.directions = "This role shouldn't show up in the list."
        self.modifiers = list()


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
