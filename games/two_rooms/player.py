class Player:
    def __init__(self, discord_user, role):
        self.user = discord_user
        self.role = role

    async def get_dm_channel(self):
        if self.user.dm_channel:
            return self.user.dm_channel
        return await self.user.create_dm()
