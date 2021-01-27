from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles import *  # pylint: disable=unused-wildcard-import

# Register all available roles. omit the word role from their name to save user input
ROLE_FACTORY = {c.__name__.lower()[:-4]: c
                for c in BaseRole.__subclasses__()}


class Player:
    def __init__(self, discord_user, role):
        self.user = discord_user
        self.role = role


class RoleManager:
    # TODO does this need a lock?
    def __init__(self):
        self.role_factory = ROLE_FACTORY
        self.unassigned_roles = list()
        self.players = list()

    def add_role(self, role):
        new_role = self.role_factory[role]()
        if new_role.max_role_count == 0:
            self.unassigned_roles.append(new_role)
            return
        count = sum(1 for i in self.unassigned_roles if i.name == new_role.name)
        if count <= new_role.max_role_count:
            self.unassigned_roles.append(new_role)

    def remove_role(self, role):
        role_to_delete = None
        for r in self.unassigned_roles:
            if r.name.lower() == role.lower():
                role_to_delete = r
                break
        if role_to_delete is not None:
            self.unassigned_roles.remove(role_to_delete)
