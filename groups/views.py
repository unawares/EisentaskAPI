from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import detail_route
from .models import MemberCard
from .models import Group
from .serializers import MemberCardSerializer
from .serializers import GroupSerializer
from .serializers import UsernameOrEmailSerializer
from .paginations import GroupsSetPagination
from .actions import GroupAdminActions
from .exceptions import GroupAdminActionsError
from .exceptions import GroupAdminActionsOnUserError

# Create your views here.

class MyGroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()

    def get_queryset(self):
        return self.queryset.filter(admin=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(admin=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @detail_route(methods=['post'], serializer_class=UsernameOrEmailSerializer)
    def add(self, request, pk=None):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(),
            Q(username=serializer.data['username_or_email'])
            | Q(email=serializer.data['username_or_email'])
        )
        result = GroupAdminActions(admin, group).actions_with(user).add()
        if not result.is_created():
            raise GroupAdminActionsOnUserError('Member already exists.')
        member_card = result.get_member_card()
        headers = self.get_success_headers(serializer.data)
        serializer = MemberCardSerializer(member_card)
        return Response(serializer.data, headers=headers)

    @detail_route(methods=['post'], serializer_class=UsernameOrEmailSerializer)
    def remove(self, request, pk=None):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(),
            Q(username=serializer.data['username_or_email'])
            | Q(email=serializer.data['username_or_email'])
        )
        member_card = GroupAdminActions(admin, group).actions_with(user).remove().get_member_card()
        headers = self.get_success_headers(serializer.data)
        serializer = MemberCardSerializer(member_card)
        return Response(serializer.data, headers=headers)

    @detail_route(methods=['post'], serializer_class=UsernameOrEmailSerializer)
    def make_staff(self, request, pk=None):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(),
            Q(username=serializer.data['username_or_email'])
            | Q(email=serializer.data['username_or_email'])
        )
        member_card = GroupAdminActions(admin, group).actions_with(user).make_user_staff().get_member_card()
        headers = self.get_success_headers(serializer.data)
        serializer = MemberCardSerializer(member_card)
        return Response(serializer.data, headers=headers)

    @detail_route(methods=['post'], serializer_class=UsernameOrEmailSerializer)
    def remove_staff(self, request, pk=None):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(),
            Q(username=serializer.data['username_or_email'])
            | Q(email=serializer.data['username_or_email'])
        )
        member_card = GroupAdminActions(admin, group).actions_with(user).remove_staff_from_user().get_member_card()
        headers = self.get_success_headers(serializer.data)
        serializer = MemberCardSerializer(member_card)
        return Response(serializer.data, headers=headers)

    @detail_route(methods=['post'], serializer_class=UsernameOrEmailSerializer)
    def make_admin(self, request, pk=None):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(),
            Q(username=serializer.data['username_or_email'])
            | Q(email=serializer.data['username_or_email'])
        )
        member_card = GroupAdminActions(admin, group).actions_with(user).give_admin_priviligies().get_member_card()
        headers = self.get_success_headers(serializer.data)
        serializer = MemberCardSerializer(member_card)
        return Response(serializer.data, headers=headers)


class MyMemberCardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MemberCardSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MemberCard.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @detail_route(methods=['delete'])
    def remove(self, request, pk=None):
        member_card = get_object_or_404(self.get_queryset(), pk=pk)
        if member_card.group.admin == member_card.owner:
            raise GroupAdminActionsError('Admin of the group could not leave, please give your admin privileges to another person to leave')
        serializer = self.get_serializer(member_card)
        member_card.delete()
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = GroupsSetPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(is_public=True) | Q(member_cards__owner=self.request.user)
            ).distinct()
        else:
            return self.queryset.filter(is_public=True)


class GroupMemberCardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemberCard.objects.all()
    pagination_class = GroupsSetPagination
    serializer_class = MemberCardSerializer

    def _get_group_instance(self, group_pk=None):
        if self.request.user.is_authenticated:
            groups = Group.objects.filter(
                Q(is_public=True) | Q(member_cards__owner=self.request.user))
        else:
            groups = Group.objects.filter(is_public=True)
        groups = groups.distinct()
        return get_object_or_404(groups, pk=group_pk)


    def get_queryset(self):
        try:
            group_pk = int(self.kwargs['group_pk'])
        except ValueError:
            group_pk = None
        group = self._get_group_instance(group_pk)
        return group.member_cards.all()
