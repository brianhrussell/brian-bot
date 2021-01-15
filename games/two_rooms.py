from games.joinable_game import JoinableGame

"""
ok so this is where all the game rules start
we may need to start breaking out more classes because
it will probably be too complex for just command handlers.

My idea here is to have a json file with all the possible cards and a class
that parses that json and knows how each of the cards interact?
    So this class will just handle which state of the game are we in
    and possibly the room leadership?
    
It can ask the RuleBook or RoleNegotiator orv whatever i end up calling it
what cards exist then offering those all as options to add. When two players share
cards or a role uses their power this class will ask the rule class what the consequences
of that action are and that action may be passed through to another class that will
actually manage the state of discord? that would help decouple this from discord at least somewhat
Then, possible

"""


class TwoRooms(JoinableGame):
    def __init__(self, guild, user):
        super().__init__(guild, user)
        self.players = dict()

    # TODO this is so sus just make the available_commands() for each game static right?
    def available_commands(self):
        for command in super().available_commands():
            yield command
