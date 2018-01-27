from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from .models import MemberCard
from .models import Group
from .serializers import MemberCardSerializer
from .serializers import GroupSerializer
from .paginations import GroupsSetPagination

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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyMemberCardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MemberCardSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MemberCard.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = GroupsSetPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(is_public=True) | Q(member_cards__owner=self.request.user)
            )
        else:
            return self.queryset.filter(is_public=True)


class GroupMemberCardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemberCard.objects.all()
    pagination_class = GroupsSetPagination
    serializer_class = MemberCardSerializer

    def get_group_instance(self, group_pk=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(Group,
                (Q(is_public=True) & Q(pk=group_pk))
                | (Q(member_cards__owner=self.request.user) & Q(pk=group_pk))
            )
        else:
            return get_object_or_404(Group,
                (Q(is_public=True) & Q(pk=group_pk))
            )

    def get_queryset(self):
        try:
            group_pk = int(self.kwargs['group_pk'])
        except ValueError:
            group_pk = None
        group = self.get_group_instance(group_pk)
        return group.member_cards.all()
