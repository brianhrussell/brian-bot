import game_tracker
import games
import settings
from games.base_game import BaseGame
from utils import get_emoji

from commands.base_command import BaseCommand


class EndGame(BaseCommand):

    def __init__(self):
        description = 'Start a game.'
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):

        guild = message.guild
        author = message.author
        if guild not in game_tracker.global_tracker.guild_mapping:
            msg = 'Couldn\'t find a game running in this server'
            await BaseCommand.send_response(msg, message.channel)
            return
        try:
            # TODO add confirmation arg or something
            game = game_tracker.get_game_for_guild(guild)
            if author.id != game.leader.id and not _user_is_admin(author):
                msg = f'you do not have persmission to end this game. ask the leader of the game or a server Administrator'
                await BaseCommand.send_response(msg, message.channel)
                return

            game.end(client)

            removed_name = game_tracker.global_tracker.remove_game(guild)
            msg = f'ended the game {removed_name}'
            await BaseCommand.send_response(msg, message.channel)
            return
        except Exception:
            possible_game_names = game_tracker.GAMES_LIST
            msg = 'something was wrong with that command try using one of these games:' \
                + f'```{ " ".join(possible_game_names) }```'
            await BaseCommand.send_response(msg, message.channel)


def _user_is_admin(user):
    return user.guild_permissions.administrator


def _construct_game_moderator(game_name, guild, game_leader):
    for g in BaseGame.__subclasses__():
        if g.__name__.lower() == game_name:
            return g(guild, game_leader)
