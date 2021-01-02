from games.base_game  import BaseGame

class ExampleGame(BaseGame):
    description = "test game"
    def __init__(self, guild, user):
        super().__init__(guild, user)
