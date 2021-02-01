from enum import Enum
from random import choice

from discord import Forbidden
from events import Events

from games.joinable_game import GameCommand, JoinableGame
from games.two_rooms.role_tracker import RoleTracker
from games.two_rooms.room import Room

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
        self.events = Events()
        self.players = dict()  # dict of discord_user : tworooms.player.Player
        self.state = TwoRoomsState.SETUP
        self.role_tracker = RoleTracker()
        self.rooms = [Room(self), Room(self)]
        self.round = 0
        self.start_channel = None

    # TODO this is so sus just make the available_commands() for each game static right?
    # consider returning only commands valid in this state
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
        yield GameCommand('send', TwoRooms.set_sent_hostage, 'chooses a player to send as a hostage at the end of this round')

    def assign_roles(self):
        for user in self.joined_users:
            self.players[user] = self.role_tracker.deal_role(user)

    async def assign_rooms(self):
        unassigned_players = list()
        for player in self.players.values():
            unassigned_players.append(player)
        num_players = len(unassigned_players)
        room_one_slots = num_players // 2
        while room_one_slots > 0:
            random_player = choice(unassigned_players)
            unassigned_players.remove(random_player)
            await self.rooms[0].add_player(random_player)
            room_one_slots = room_one_slots - 1
        for player in unassigned_players:
            await self.rooms[1].add_player(player)

    def assign_leaders_randomly(self):
        for room in self.rooms:
            room.leader = choice(room.players)

    def get_room_for_player(self, player):
        for room in self.rooms:
            if player in room.players:
                return room
        return None

    def are_hostages_valid(self, room, mentions):
        if len(mentions) != self.get_hostages_per_round():
            return False
        for user in mentions:
            player = self.players[user]
            if player is room.leader or player not in room.players:
                return False
        return True

    ''' get_hostages_per_round chart
    round     1   2   3
    6-10      1   1   1
    11-21     2   1   1
    22+       3   2   1
    '''

    def get_hostages_per_round(self):
        num_players = len(self.players)
        game_size = num_players // 11
        return max(game_size + 2 - self.round, 1)

    async def end_round(self):
        await self.exchange_hostages()
        self.round += 1
        await self.events.fire('on_round_start', self.round)

    async def exchange_hostages(self):
        send_to_two = self.rooms[0].next_sent_hostages
        send_to_one = self.rooms[1].next_sent_hostages
        for user in send_to_two:
            player = self.players[user]
            await self.rooms[0].remove_player(player)
            await self.rooms[1].add_player(player)
        for user in send_to_one:
            player = self.players[user]
            await self.rooms[1].remove_player(player)
            await self.rooms[0].add_player(player)
        self.rooms[0].next_sent_hostages.clear()
        self.rooms[1].next_sent_hostages.clear()

# COMMAND HANDLERS
    def set_room_roles(self, params, message, client):
        if self.state != TwoRoomsState.SETUP:
            return 'not a valid state to setup channels'
        if message.author.id != self.leader.id:
            return 'only the leader can set the room roles'
        if len(message.role_mentions) != 2:
            'please mention exactly two roles to set roles'
        self.rooms[0].set_role(message.role_mentions[0])
        self.rooms[1].set_role(message.role_mentions[1])
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

    async def begin_game(self, params, message, client):
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
        if not (self.rooms[0].discord_role and self.rooms[1].discord_role):
            return 'you need to set a role for each room. use `!game room-roles @role1 @role2`'
        if player_id != self.leader.id:
            return 'only the leader can start the game'
        try:
            self.start_channel = message.channel
            self.assign_roles()
            await self.assign_rooms()
            self.state = TwoRoomsState.PLAYING
            self.round = 1
            self.assign_leaders_randomly()
            self.events.register('on_hostages_set', self.on_hostages_set_event)
            self.events.register('on_round_start', self.on_round_start_event)
            await self.events.fire('on_round_start', 1)
        except Forbidden as e:
            return f'the bot is missing the permissions it needs message: {e}'

    async def set_sent_hostage(self, params, message, client):
        if self.state != TwoRoomsState.PLAYING:
            return 'game needs to be started to designate a hostage'
        player = self.players[message.author]
        room = self.get_room_for_player(player)
        if room is None or room.leader != player:
            return 'you are not the room leader'
        if not self.are_hostages_valid(room, message.mentions):
            return f'invalid hostages. you need to send {self.get_hostages_per_round()} and the leader can\'t send themself'
        await room.set_next_hostages(message.mentions)
        return 'hostages set. they will be sent when the other room is ready. you can still change them in the meantime.'

# EVENT HANDLERS
    async def on_hostages_set_event(self, room):
        if self.rooms[0].next_sent_hostages and self.rooms[1].next_sent_hostages:
            await self.end_round()

    async def on_round_start_event(self, round_number):
        if round_number < 4:
            return
        msg = ['game has finished']
        msg.append('room 1:')
        msg.append(self.rooms[0].get_room_status())
        msg.append('room 2:')
        msg.append(self.rooms[1].get_room_status())
        self.start_channel.send('\n'.join(msg))
