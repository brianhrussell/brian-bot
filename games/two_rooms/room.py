import discord


class Room:
    def __init__(self):
        self.players = list()
        self.role = None
        self.text_channels = list()
        self.voice_channels = list()

    def add_player(self, player):
        player.add_role(self.role)
        self.players.append(player)

    def remove_player(self, player):
        player.remove_role(self.role)
        self.players.remove(player)
