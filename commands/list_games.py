import games
from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint



class ListGames(BaseCommand):

    def __init__(self):
        description = "Lists the games this bot can play"
        params = []
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        from game_tracker import GAME_LIST
        msg = message.author.mention + "\n"

        # Displays all descriptions, sorted alphabetically by command name
        for game in sorted(GAME_LIST.items()):
            msg += "\n" + game[1].description

        await message.channel.send(msg)
    