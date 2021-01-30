import discord


class Room:
    def __init__(self):
        self.players = list()
        self.text_channels = list()
        self.voice_channels = list()
