import discord


class Room:
    def __init__(self):
        self.players = list()
        self.role = None
        self.text_channels = list()
        self.voice_channels = list()
