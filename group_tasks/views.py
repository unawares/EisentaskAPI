from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from groups.models import Group
from .models import GroupTask
from .models import CompletedGroupTask
from .serializers import GroupTaskSerializer
from .paginations import PrioritizedActiveTasksSetPagination

# Create your views here.

class GroupTasksViewSet(viewsets.GenericViewSet):
    serializer_class = GroupTaskSerializer
    pagination_class = PrioritizedActiveTasksSetPagination
    queryset = GroupTask.objects.all()

    def _get_group_instance(self, group_pk=None):
        if self.request.user.is_authenticated:
            groups = Group.objects.filter(
                Q(is_public=True) | Q(member_cards__owner=self.request.user))
        else:
            groups = Group.objects.filter(is_public=True)
        return get_object_or_404(groups, pk=group_pk)

    def _get_queryset(self):
        group = self._get_group_instance(group_pk=int(self.kwargs['group_id']))
        group_tasks = self.queryset.filter(group=group)
        if 'priority' in self.kwargs:
            group_tasks = group_tasks.filter(priority=self.kwargs['priority'])
        if self.request.user.is_authenticated:
            completed_shared_tasks = CompletedGroupTask.objects.filter(
                owner=self.request.user,
                group=group,
            ).values_list('shared_task', flat=True)
            group_tasks = group_tasks.exclude(shared_task__in=completed_shared_tasks)
        return group_tasks

    def list_by_priority(self, request, *args, **kwargs):
        queryset = self._get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, type, group_id, pk):
        shared_task = get_object_or_404(self._get_queryset(), pk=pk)
        serializer = self.serializer_class(shared_task)
        return Response(serializer.data)
