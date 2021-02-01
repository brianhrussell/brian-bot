class Player:
    def __init__(self, discord_user):
        self.user = discord_user
        self.role = None
        self.discord_role = None

    async def set_role(self, role):
        msg = list()
        if self.role is not None:
            # TODO more info here
            msg.append('your role has changed')
        msg.append('your role is:')
        msg.append(role.to_string())
        dm = await self.get_dm_channel()
        await dm.send('\n'.join(msg))

    async def get_dm_channel(self):
        if self.user.dm_channel:
            return self.user.dm_channel
        return await self.user.create_dm()

    async def add_discord_role(self, role):
        await self.user.add_roles(role)

    async def remove_discord_role(self, role):
        await self.user.remove_roles(role)
