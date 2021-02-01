from random import choice
from threading import Lock

from games.two_rooms.player import Player
from games.two_rooms.roles import *  # pylint: disable=unused-wildcard-import
from games.two_rooms.roles.role_utils import BaseRole

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

    def roles_are_valid(self, num_players):
        roles_in_set = len(self.unassigned_roles)
        if roles_in_set < num_players:
            return False
        any_roles_allow_buried_card = False
        for role in self.unassigned_roles:
            if role.allows_buried_role:
                any_roles_allow_buried_card = True
            if not self.required_roles_are_met(role):
                return False

        # TODO implement requires bury card
        if any_roles_allow_buried_card:
            return roles_in_set - 1 <= num_players
        return roles_in_set == num_players

    def required_roles_are_met(self, role):
        for required_role in role.required_roles:
            if not any(r.name.lower() == required_role.lower() for r in self.unassigned_roles):
                return False
        return True

    def deal_role(self, discord_user):
        dealt_role = choice(self.unassigned_roles)
        self.unassigned_roles.remove(dealt_role)
        return Player(discord_user, dealt_role)
