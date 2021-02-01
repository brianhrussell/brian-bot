import discord


class Room:
    def __init__(self, game):
        self.players = list()
        self.discord_role = None
        self.channel = None
        self.leader = None
        game.events.register('on_round_start', self.on_round_start_event)

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

    async def on_round_start_event(self, round_number):
        msg = [f'start of round {round_number}']
        msg.append(f'leader is {self.leader.user.mention}')
        msg.append('players in this room:')
        for player in self.players:
            if player is self.leader:
                continue
            msg.append(player.user.mention)
        await self.send_message('\n'.join(msg))

    def guess_main_channel(self):
        channels = self.discord_role.guild.channels
        for channel in channels:
            if type(channel) is not discord.TextChannel or self.discord_role not in channel.overwrites:
                continue
            if channel.overwrites[self.discord_role].send_messages:
                return channel
        raise 'could not guess the main channel for the room sorry ask brian'
