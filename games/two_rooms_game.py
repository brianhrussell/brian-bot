from games.joinable_game import JoinableGame
from games.joinable_game import GameCommand
from games.two_rooms.role_tracker import RoleTracker
from games.two_rooms.room import Room
from math import floor, ceil
from random import randrange
from enum import Enum
from random import choice
from discord import Forbidden
from events import Events

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


class TwoRoomsState(Enum):
    SETUP = 0
    PLAYING = 1


class TwoRooms(JoinableGame):

    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.players = dict()  # dict of discord_user : tworooms.player.Player
        self.state = TwoRoomsState.SETUP
        self.role_tracker = RoleTracker()
        self.rooms = [Room(), Room()]
        self.round = 0

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
        yield GameCommand('room-roles', TwoRooms.set_room_roles, 'assigns a channel to a room')

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
            self.rooms[0].add_player(unassigned_players.pop(rand_index))
            room_one_slots = room_one_slots - 1
        for player in unassigned_players:
            self.rooms[1].add_player(player)

    def assign_leaders_randomly(self):
        for room in self.rooms:
            room_size = len(room.players)
            room.leader = room.players[randrange(0, room_size)]

    # COMMAND HANDLERS
    def set_room_roles(self, params, message, client):
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to setup channels'
        if message.author.id != self.leader.id:
            return 'only the leader can set the room roles'
        if len(message.role_mentions) != 2:
            'please mention exactly two roles to set roles'
        self.rooms[0].role = message.role_mentions[0]
        self.rooms[1].role = message.role_mentions[1]
        return 'roles set successfully. you should double check that these roles each' +\
            ' have at least one text channel that they can see and the other cannot'

    def add_role(self, params, message, client):
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to add a role'

        if len(params) == 0:
            return 'provide a role name to add try using `!game list-roles`'
        for param in params:
            if param.lower() not in self.role_tracker.role_factory:
                return f'{param} is not a valid role. use  `!game list-roles` to see a list of available roles.'
            self.role_tracker.add_role(param.lower())
            return f'added roles successfully. current play set size: {len(self.role_tracker.unassigned_roles)}'

    def remove_role(self, params, message, client):
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to remove a role'

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
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to remove roles'
        self.role_tracker.clear_roles()
        return 'play set cleared'

    def selected_roles(self, params, message, client):
        roles = self.role_tracker.get_selected_role_names()
        return 'selected roles:\n' + roles

    def begin_game(self, params, message, client):
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to begin a game'
        player_id = message.author.id
        num_players = len(self.joined_users)
        if num_players < 4:
            return 'you need more people to play'
        if not self.role_tracker.roles_are_valid(num_players):
            return "the selected roles are not valid sorry," + \
                " you'll have to figure out why on your own. selected roles:\n" + \
                self.role_tracker.get_selected_role_names()
        if not (self.rooms[0].role and self.rooms[1].role):
            return 'you need to set a role for each room. use `!game room-roles @role1 @role2`'
        if player_id != self.leader.id:
            return 'only the leader can start the game'
        try:
            self.assign_roles()
            self.assign_rooms()
            self.state = TwoRoomsState.PLAYING
            self.round = 1
            self.assign_leaders_randomly()
        except Forbidden as e:
            return f'the bot is missing the permissions it needs message: {e}'
