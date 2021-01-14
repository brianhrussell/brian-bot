import threading
from multiprocessing import Pool

from games import *                     # pylint: disable=unused-wildcard-import
from games.base_game import BaseGame

# global tracking of the games that are build run in each guild.
# use as global singleton global_tracker
# how to track dms? can do just context? or maybe dm response always have a canned id?
# this is supposed to be a singleton more or less
GAMES_LIST = [g.__name__.lower() for g in BaseGame.__subclasses__()]


class GameTracker:

    def __init__(self):
        self.supported_games = GAMES_LIST
        self.game_tracker_lock = threading.Lock()
        self.guild_mapping = dict()

    def ensure_mapping_exists(self):
        self.game_tracker_lock.acquire()
        if self.guild_mapping is None:
            self.guild_mapping = dict()
        self.game_tracker_lock.release()

    def add_game(self, guild, game):
        self.ensure_mapping_exists()
        self.game_tracker_lock.acquire()
        self.guild_mapping[guild] = game
        self.game_tracker_lock.release()
        return game

    def remove_game(self, guild):
        if self.guild_mapping is None:
            return
        self.game_tracker_lock.acquire()
        game = self.guild_mapping.pop(guild)
        name = game.name
        del(game)
        self.game_tracker_lock.release()
        return name

    def remove_all_games(self):
        self.game_tracker_lock.acquire()
        self.guild_mapping.clear()
        self.game_tracker_lock.release()


global_tracker = GameTracker()


def get_game_for_guild(guild):
    return global_tracker.guild_mapping[guild]
