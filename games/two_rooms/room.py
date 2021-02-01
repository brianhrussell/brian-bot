import discord


class Room:
    def __init__(self, game):
        self.players = list()
        self.discord_role = None
        self.channel = None
        self.leader = None
        self.next_sent_hostages = list()
        self.events = game.events
        self.events.register('on_round_start', self.on_round_start_event)
        self.events.register('on_hostages_set', self.on_hostages_set_event)

    async def send_message(self, message):
        await self.channel.send(message)

    def set_role(self, role):
        self.discord_role = role
        self.channel = self.guess_main_channel()

    async def add_player(self, player):
        await player.add_discord_role(self.discord_role)
        self.players.append(player)

    async def remove_player(self, player):
        await player.remove_discord_role(self.discord_role)
        self.players.remove(player)

    def guess_main_channel(self):
        channels = self.discord_role.guild.channels
        for channel in channels:
            if type(channel) is not discord.TextChannel or self.discord_role not in channel.overwrites:
                continue
            if channel.overwrites[self.discord_role].send_messages:
                return channel
        raise 'could not guess the main channel for the room sorry ask brian'

    async def set_next_hostages(self, mentions):
        if len(self.next_sent_hostages) == 0:
            self.events.fire('on_hostages_set', self)
        self.next_sent_hostages = mentions

    def get_room_status(self):
        status = list()
        status.append(f'leader is {self.leader.user.mention}')
        status.append('players in this room:')
        for player in self.players:
            if player is self.leader:
                continue
            status.append(player.user.mention)
        return '\n'.join(status)

# EVENT HANDLERS

    async def on_hostages_set_event(self, room):
        if room is self:
            return
        await self.channel.send('the other room has picked their hostage(s).')

    async def on_round_start_event(self, round_number):
        if round_number > 3:
            return
        msg = [f'start of round {round_number}']
        msg.append(self.get_room_status())
        await self.send_message('\n'.join(msg))
