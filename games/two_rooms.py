from games.joinable_game import JoinableGame


class TwoRooms(JoinableGame):
    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.players = dict()

    def available_commands(self):
        yield super().available_commands()
        yield JoinableGame.join_command
