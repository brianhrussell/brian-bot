import games
import game_tracker
from commands.base_command import BaseCommand
from utils import get_emoji
from random import randint


class ListGames(BaseCommand):

    def __init__(self):
        description = "Lists the games this bot can play"
        params = []
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        msg = 'Supported games:'
        # Displays all descriptions, sorted alphabetically by command name
        # TODO: add detail to game modules and print it here
        for game in sorted(game_tracker.GAMES_LIST):
            msg += "\n" + game

        await BaseCommand.send_response(msg, message.channel)
