import games
import settings
from commands.base_command import BaseCommand
from utils import get_emoji
import game_tracker


class G(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = 'Send a command to a game. Query the specific module for more info'
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

        if guild not in game_tracker.global_tracker.guild_mapping:
            msg = f'no game currently running in this server try starting one with {settings.COMMAND_PREFIX}startgame'
            await BaseCommand.send_response(msg, message.channel)
            return
        game_manager = game_tracker.get_game_for_guild(guild)

        msg = await game_manager.handle_message(params, message, client)
        await BaseCommand.send_response(msg, message.channel)

    @staticmethod
    def pass_command_to_game(game, params, message, client):
        command = params[0]
        for available_command in game.available_commands():
            if command == available_command.command:
                return available_command.func(game, params[1::], message, client)

        return (f'there isn\'t an available command for this game with keyword "{command}"')
