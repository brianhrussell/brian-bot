from threading import Lock


from games.two_rooms.roles.role_utils import BaseRole
from games.two_rooms.roles import *  # pylint: disable=unused-wildcard-import

# Register all available roles. omit the word role from their name to save user input
ROLE_FACTORY = {c.__name__.lower()[:-4]: c
                for c in BaseRole.__subclasses__()}


class RoleTracker:
    #  does this need a lock?
    def __init__(self):
        self.role_factory = ROLE_FACTORY
        self.unassigned_roles = list()
        self.players = list()
        self.lock = Lock()

    def add_role(self, role):
        with self.lock:
            new_role = self.role_factory[role]()
            if new_role.max_role_count == 0:
                self.unassigned_roles.append(new_role)
                return
            count = sum(1 for i in self.unassigned_roles if i.name == new_role.name)
            if count <= new_role.max_role_count:
                self.unassigned_roles.append(new_role)

    def remove_role(self, role):
        with self.lock:
            role_to_delete = None
            for r in self.unassigned_roles:
                if r.name.lower() == role.lower():
                    role_to_delete = r
                    break
            if role_to_delete is not None:
                self.unassigned_roles.remove(role_to_delete)

    def clear_roles(self):
        with self.lock:
            self.unassigned_roles.clear()

    def get_selected_role_names(self):
        selected_roles = list()
        for role_name in self.role_factory:
            count = sum(1 for i in self.unassigned_roles if i.name.lower() == role_name.lower())
            if count != 0:
                selected_roles.append(role_name + f' x{count}')
        return '\n'.join(selected_roles)

    def roles_are_valid(self):
        return False
