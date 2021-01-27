import game_tracker
import games
import settings
from games.base_game import BaseGame
from utils import get_emoji

from commands.base_command import BaseCommand
from game_tracker import all_subclasses


class StartGame(BaseCommand):

    def __init__(self):
        description = 'Start a game.'
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):

        guild = message.guild

        if guild in game_tracker.global_tracker.guild_mapping:
            msg = 'there is already a game running in this server try again after it\'s' \
                + 'over or ask the leader or a server admin to end it if it has been abandoned'
            await BaseCommand.send_response(msg, message.channel)
            return
        try:
            game_name = params[0]
            # start a game in the tracker and set the leader to this user
            game_leader = message.author
            game_moderator = _construct_game_moderator(game_name, guild, game_leader)
            game = game_tracker.global_tracker.add_game(guild, game_moderator)
            game.start(client)
            msg = f'started the game {game_name}'
            await BaseCommand.send_response(msg, message.channel)
            return
        except Exception:  # TODO don't catch Exception
            possible_game_names = game_tracker.GAMES_LIST
            msg = 'something was wrong with that command try using one of these games:' \
                + f'```{ " ".join(possible_game_names) }```'
            await BaseCommand.send_response(msg, message.channel)


def _construct_game_moderator(game_name, guild, game_leader):
    for g in all_subclasses(BaseGame):
        if g.__name__.lower() == game_name:
            return g(guild, game_leader)
    raise 'game not found'
