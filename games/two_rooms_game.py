from games.joinable_game import JoinableGame
from games.joinable_game import GameCommand
from enum import Enum
import games.two_rooms.players
"""
ok so this is where all the game rules start
we may need to start breaking out more classes because
it will probably be too complex for just command handlers.

My idea here is to have a json file with all the possible cards and a class
that parses that json and knows how ea  ch of the cards interact?
    So this class will just handle which state of the game are we in
    and possibly the room leadership?
    
It can ask the RuleBook or RoleNegotiator orv whatever i end up calling it
what cards exist then offering those all as options to add. When two players share
cards or a role uses their power this class will ask the rule class what the consequences
of that action are and that action may be passed through to another class that will
actually manage the state of discord? that would help decouple this from discord at least somewhat
Then, possible

"""


class TwoRooms(JoinableGame):

    class TwoRoomsState(Enum):
        SETUP = 0
        ON_BEGIN = 1

    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.players = dict()
        self.state = TwoRooms.TwoRoomsState.SETUP

    # TODO this is so sus just make the available_commands() for each game static right?
    def available_commands(self):
        for command in super().available_commands():
            yield command
        yield TwoRooms.begin_game
        yield GameCommand('begin', TwoRooms.begin_game, 'once all players and roles have been added begin the game and assign roles')

    def selected_roles_are_valid(self):
        raise NotImplementedError
        # return true

    def assign_roles(self):
        raise NotImplementedError

    def begin_game(self, params, message, client):
        player_id = message.author.id
        if not self.selected_roles_are_valid():
            return "the selected roles are not valid sorry," + \
                " you'll have to figure out why on your own. selected roles: TODO print selected roles"
        if player_id == self.leader.id:
            self.assign_roles()
