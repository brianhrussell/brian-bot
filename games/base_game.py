import settings
from discord import User
from discord import Guild

class BaseGame:
    # base class for a game. base requires a guild and a player to start it
    def __init__(self, guild, user):
        if not (guild is Guild):
            raise "attempted to create game with invalid guild"
        if not (user is User):
            raise "attempted to create game with invalid User"
        self.guild = guild
        self.leader = user
        self.players = [user]
        self.phases = ['adding players']
        self.name = "BaseGame"
