from games.base_game import BaseGame
from games.base_game import GameCommand


class JoinableGame(BaseGame):

    # TODO: uhhh this probably regenerates this list every time? performance check this later
    def available_commands(self):
        yield JoinableGame.join_command

    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.players = dict()

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
        player_id = message.author.id
        player = message.author
        if player_id in self.players:
            # TODO test this >_>
            return f'{player} has already joined.'
        self.players[player_id] = player
        return(f'added {player} to the game.')

    join_command = GameCommand('join', 'join a game in progress', join_game)
