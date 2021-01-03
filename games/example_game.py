from games.base_game import BaseGame


class ExampleGame(BaseGame):
    description = "test game"

    def __init__(self, guild, user):
        super().__init__(guild, user)

    def handle_message(self, message, client):
        raise NotImplementedError  # To be defined by every event

    def start(self, client):
        print
