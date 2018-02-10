from django.contrib.auth import get_user_model
from .models import Group
from .models import MemberCard
from .exceptions import GroupAdminActionsError
from .exceptions import GroupAdminActionsOnUserError
from .exceptions import GroupAdminActionsNoMemberError

class GroupAdminActions:
    class Actions:
        class MemberCard:
            def __init__(self, member_card, created=False):
                self.member_card = member_card
                self.created = created

            def get_member_card(self):
                return self.member_card

            def is_created(self):
                return self.created

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
                raise GroupAdminActionsNoMemberError('User must be member of the group.')
            return member_card

        def add(self):
            member_card, created = MemberCard.objects.get_or_create(
                group = self.group,
                owner = self.user,
            )
            member_card.is_staff = False
            member_card.save()
            return GroupAdminActions.Actions.MemberCard(member_card, created)

        def remove(self):
            member_card = MemberCard.objects.filter(group = self.group,
                                                    owner = self.user,)
            member_card.delete()
            return GroupAdminActions.Actions.MemberCard(member_card)

        def make_user_staff(self):
            member_card = self._get_member_card()
            member_card.is_staff = True
            member_card.save()
            return GroupAdminActions.Actions.MemberCard(member_card)

        def remove_staff_from_user(self):
            member_card = self._get_member_card()
            member_card.is_staff = False
            member_card.save()
            return GroupAdminActions.Actions.MemberCard(member_card)

        def give_admin_priviligies(self):
            member_card = self._get_member_card()
            member_card.is_staff = True
            member_card.save()
            self.group.admin = self.user
            self.group.save()
            return GroupAdminActions.Actions.MemberCard(member_card)


    def __init__(self, admin, group):
        if not admin == group.admin:
            raise GroupAdminActionsError('User has not admin privileges.')
        self.admin = admin
        self.group = group

    def actions_with(self, user):
        if self.admin == user:
            raise GroupAdminActionsOnUserError('User has admin privileges.')
        return GroupAdminActions.Actions(self.admin, self.group, user)
