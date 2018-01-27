from django.contrib.auth import get_user_model
from .models import Group
from .models import MemberCard

class GroupAdminActions:
    class GroupAdminActionsError(Exception):
        pass

    class Actions:
        def __init__(self, admin, group, user):
            self.admin = admin
            self.group = group
            self.user = user

        def _get_member_card(self):
            try:
                member_card = MemberCard.objects.get(
                    group = self.group,
                    owner = self.user,
                )
            except MemberCard.DoesNotExist:
                raise GroupAdminActionsError('User must be member of the group')
            return member_card

        def add(self):
            member_card, created = MemberCard.objects.get_or_create(
                group = self.group,
                owner = self.user,
            )
            member_card.is_staff = False
            member_card.save()

        def make_user_staff(self):
            member_card = self._get_member_card()
            member_card.is_staff = True
            member_card.save()

        def remove_staff_from_user(self):
            member_card = self._get_member_card()
            member_card.is_staff = False
            member_card.save()

        def give_admin_priviligies(self):
            member_card = self._get_member_card()
            self.group.admin = self.user
            self.group.save()


    def __init__(self, admin, group):
        if not admin == group.admin:
            raise GroupAdminActionsError('User does not have admin privileges.')
        self.admin = admin
        self.group = group

    def actions_with(self, user):
        return GroupAdminActions.Actions(self.admin, self.group, user)
