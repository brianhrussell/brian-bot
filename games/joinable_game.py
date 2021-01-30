from games.base_game import BaseGame
from games.base_game import GameCommand
from enum import Enum


class JoinableGame(BaseGame):

    class JoinableGameState(Enum):
        SETUP = 0

    # TODO: uhhh this probably regenerates this list every time? performance check this later

    def available_commands(self):
        yield JoinableGame.join_command

    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.joined_users = dict()
        self.state = self.JoinableGameState.SETUP  # to be overwritten but subclasses with actual state enums

    # TODO this should probably be higher in the class hierarchy
    def handle_message(self, params, message, client):
        command = params[0]
        for available_command in self.available_commands():
            if command == available_command.command:
                return available_command.func(self, params[1::], message, client)

        return (f'there isn\'t an available command for this game with keyword "{command}"')

    def start(self, client):
        print('joinable game started')

    def end(self, client):
        print('joinable game ended')

    def join_game(self, params, message, client):
        # make a separate function on the game that returns whether a player can be added rather than relying on state
        if self.state.value != 0:
            return "game has already started, we can't add you"
        player_id = message.author.id
        player = message.author
        if player_id in self.joined_users:
            # TODO test this >_>
            return f'{player} has already joined.'
        self.joined_users[player_id] = player
        return(f'added {player} to the game.')

    join_command = GameCommand('join', join_game, 'join a game in progress')
