from games.joinable_game import JoinableGame
from games.joinable_game import GameCommand
from games.two_rooms.role_tracker import RoleTracker
from games.two_rooms.room import Room
from math import floor, ceil
from random import randrange
from enum import Enum
from random import choice

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
        self.players = dict()  # dict of discord_user : tworooms.player.Player
        self.state = TwoRooms.TwoRoomsState.SETUP
        self.role_tracker = RoleTracker()
        self.rooms = [Room(), Room()]

    # TODO this is so sus just make the available_commands() for each game static right?
    def available_commands(self):
        for command in super().available_commands():
            yield command
        yield GameCommand('begin', TwoRooms.begin_game, 'once all players and roles have been added begin the game and assign roles')
        yield GameCommand('add-role', TwoRooms.add_role, 'add a role to the play set')
        yield GameCommand('remove-role', TwoRooms.remove_role, 'remove a role from the play set')
        yield GameCommand('list-roles', TwoRooms.list_roles, 'list the available roles')
        yield GameCommand('clear-roles', TwoRooms.clear_roles, 'reset the play set and start over')
        yield GameCommand('selected-roles', TwoRooms.selected_roles, 'display the roles in the current play set')

    def assign_roles(self):
        for user in self.joined_users:
            self.players[user] = self.role_tracker.deal_role(user)

    def assign_rooms(self):
        unassigned_players = list()
        for player in self.players.values():
            unassigned_players.append(player)
        num_players = len(unassigned_players)
        room_one_slots = floor(num_players / 2)
        while room_one_slots > 0:
            rand_index = randrange(0, room_one_slots)
            self.rooms[0].players.append(unassigned_players.pop(rand_index))
            room_one_slots = room_one_slots - 1
        self.rooms[1].players = unassigned_players

    def add_role(self, params, message, client):
        if len(params) == 0:
            return 'provide a role name to add try using `!game list-roles`'
        for param in params:
            if param.lower() not in self.role_tracker.role_factory:
                return f'{param} is not a valid role. use  `!game list-roles` to see a list of available roles.'
            self.role_tracker.add_role(param.lower())
            return f'added roles successfully. current play set size: {len(self.role_tracker.unassigned_roles)}'

    def remove_role(self, params, message, client):
        if len(params) == 0:
            return 'provide a role name to remove try using `!game list-roles` or clear all roles with `!game clear-roles`'
        for param in params:
            if param.lower() not in self.role_tracker.role_factory:
                return f'{param} is not a valid role. use  `!game list-roles` to see a list of available roles.'
            self.role_tracker.remove_role(param.lower())
            return 'removed roles successfully'

    def list_roles(self, params, message, client):
        lines = list()
        for role_name in self.role_tracker.role_factory:
            role = self.role_tracker.role_factory[role_name]()
            lines.append(role.to_string())
        return '\n\n'.join(lines)

    def clear_roles(self, params, message, client):
        self.role_tracker.clear_roles()
        return 'play set cleared'

    def selected_roles(self, params, message, client):
        roles = self.role_tracker.get_selected_role_names()
        return 'selected roles:\n' + roles

    def begin_game(self, params, message, client):
        player_id = message.author.id
        num_players = len(self.joined_users)
        if num_players < 4:
            return 'you need more people to play'
        if not self.role_tracker.roles_are_valid(num_players):
            return "the selected roles are not valid sorry," + \
                " you'll have to figure out why on your own. selected roles:\n" + \
                self.role_tracker.get_selected_role_names()
        if player_id == self.leader.id:
            self.assign_roles()
            self.assign_rooms()
