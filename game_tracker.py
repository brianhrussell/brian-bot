from games.base_game import BaseGame
from games import *
import threading

# global tracking of the games that are build run in each guild. 
# use as global singleton global_tracker
# how to track dms? can do just context? or maybe dm response always have a canned id?
GAMES_LIST  = [g.__name__.lower() for g in BaseGame.__subclasses__()]

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

    def remove_game(self, guild):
        if self.guild_mapping is None:
            return
        self.game_tracker_lock.acquire()
        self.guild_mapping.pop(guild)
        self.game_tracker_lock.release()

global_tracker = GameTracker()