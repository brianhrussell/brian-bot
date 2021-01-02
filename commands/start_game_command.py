import games
import settings
from commands.base_command  import BaseCommand
from utils                  import get_emoji
import game_tracker


class StartGame(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = 'Start a game.'
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = None
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        guild = message.guild

        if guild in game_tracker.global_tracker.guild_mapping:
            msg = f'there is already a game running in this server try again after it\'s over or\
                    ask the leader or a server admin to end it if it has been abandoned \
                    (brian hasn\'t implemented this yet so get fukt lol)'
            await message.channel.send(msg)
            return
        try:
            game_name = params[0]
            # start a game in the tracker and set the leader to this user
            msg = f'started the game {game_name}'
            await message.channel.send(msg)
            return
        except:
            possible_game_names = game_tracker.GAMES_LIST
            msg = f'something was wrong with that command try using one of these games: ```' + ' '.join(possible_game_names) + '```'
            await message.channel.send(msg)
