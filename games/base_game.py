from inspect import iscoroutinefunction


class BaseGame:
    # base class for a game. base requires a guild and a player to start it
    def __init__(self, guild, user):
        self.guild = guild
        self.leader = user
        self.players = [user]
        self.states = ['adding players']
        self.name = type(self).__name__.lower()

    # Every game must override this method
    # TODO: maybe instead of the game moderator handling messages we'll
    # have the game class report what the command apis it can handle in
    # each state? so that it doesn't need to know about discord
    # but that seems impossible since it will still need to interact
    # with discord to handle the side affects of the commands.
    async def handle_message(self, params, message, client):
        raise NotImplementedError  # To be defined by every event

    def start(self, client):
        raise NotImplementedError  # To be defined by every event

    def end(self, client):
        raise NotImplementedError  # To be defined by every event

    def available_commands(self):
        raise NotImplementedError  # To be defined by every event


class GameCommand:

    def __init__(self, command, func, description):
        self.command = command
        self.func = func
        self.description = description

    async def __call__(self, *a):
        if iscoroutinefunction(self.func):
            return await self.func(*a)
        else:
            return self.func(*a)
