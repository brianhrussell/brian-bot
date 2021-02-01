import threading
from multiprocessing import Pool

from games import *  # pylint: disable=unused-wildcard-import
from games.base_game import BaseGame


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


# global tracking of the games that are build run in each guild.
# use as global singleton global_tracker
# how to track dms? can do just context? or maybe dm response always have a canned id?
# this is supposed to be a singleton more or less
GAMES_LIST = [g.__name__.lower() for g in all_subclasses(BaseGame)]

global_tracker_lock = threading.Lock()


class GameTracker:

    def __init__(self):
        self.supported_games = GAMES_LIST
        self.game_tracker_lock = global_tracker_lock
        self.guild_mapping = dict()

    def ensure_mapping_exists(self):
        with self.game_tracker_lock:
            if self.guild_mapping is None:
                self.guild_mapping = dict()

    def add_game(self, guild, game):
        self.ensure_mapping_exists()
        with self.game_tracker_lock:
            self.guild_mapping[guild] = game
        return game

    def remove_game(self, guild):
        if self.guild_mapping is None:
            return
        with self.game_tracker_lock:
            game = self.guild_mapping.pop(guild)
            if game is None:
                self.game_tracker_lock.release()
                return 'ghost game'
            name = game.name
            del(game)
        return name

    def remove_all_games(self):
        with self.game_tracker_lock:
            self.guild_mapping.clear()


global_tracker = GameTracker()


def get_game_for_guild(guild):
    return global_tracker.guild_mapping[guild]
