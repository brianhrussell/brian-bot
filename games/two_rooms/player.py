class Player:
    def __init__(self, discord_user, role):
        self.user = discord_user
        self.role = role
        self.discord_role = None

    async def get_dm_channel(self):
        if self.user.dm_channel:
            return self.user.dm_channel
        return await self.user.create_dm()

    async def add_discord_role(self, role):
        await self.user.add_roles(role)

    async def remove_discord_role(self, role):
        await self.user.remove_roles(role)
