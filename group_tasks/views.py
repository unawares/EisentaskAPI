from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from groups.models import Group
from groups.models import MemberCard
from .models import GroupTask
from .models import CompletedGroupTask
from .models import SharedTask
from .serializers import GroupTaskSerializer
from .serializers import CompletedGroupTaskSerializer
from .serializers import GroupTaskOrderSerializer
from .serializers import GroupTasksSelectionSerializer
from .paginations import PrioritizedActiveTasksSetPagination

# Create your views here.

class GroupTasksViewSet(viewsets.GenericViewSet):
    active_task_serializer_class = GroupTaskSerializer
    completed_task_serializer_class = CompletedGroupTaskSerializer
    pagination_class = PrioritizedActiveTasksSetPagination
    queryset = GroupTask.objects.all()

    def get_serializer_class(self):
        return self.active_task_serializer_class

    def _get_group_instance(self, group_pk=None):
        if self.request.user.is_authenticated:
            groups = Group.objects.filter(
                Q(is_public=True) | Q(member_cards__owner=self.request.user))
        else:
            groups = Group.objects.filter(is_public=True)
        groups = groups.distinct()
        return get_object_or_404(groups, pk=group_pk)

    def _get_queryset_active_group_tasks(self, group=None):
        active_group_tasks = self.queryset.filter(group=group)
        if 'priority' in self.kwargs:
            active_group_tasks = active_group_tasks.filter(
                                            priority=self.kwargs['priority'])
        if group.flow == 1:
            if self.request.user.is_authenticated:
                completed_shared_tasks = CompletedGroupTask.objects.filter(
                    owner=self.request.user,
                    group=group,
                ).values_list('shared_task', flat=True)
        else:
            if self.request.user.is_authenticated:
                completed_shared_tasks = CompletedGroupTask.objects.filter(
                    group=group
                ).values_list('shared_task', flat=True)
        active_group_tasks = active_group_tasks.exclude(
            shared_task__in=completed_shared_tasks)
        return active_group_tasks

    def _get_queryset_completed_group_tasks(self, group=None):
        completed_group_tasks = CompletedGroupTask.objects.filter(
            group=group
        )
        if group.flow == 1:
            completed_group_tasks = completed_group_tasks.filter(owner=self.request.user)
        return completed_group_tasks

    def _query_params_validate(self, query_params):
        errors = { 'query_params': {} }
        if 'year' in query_params:
            try:
                int(query_params['year'])
            except ValueError:
                errors['query_params']['year'] = 'Invalid value.'
        else:
            errors['query_params']['year'] = "You must set 'year' parameter."
        if 'month' in query_params:
            try:
                int(query_params['month'])
            except ValueError:
                errors['query_params']['month'] = 'Invalid value.'
        else:
            errors['query_params']['month'] = "You must set 'month' parameter."
        if 'day' in query_params:
            try:
                int(query_params['day'])
            except ValueError:
                errors['query_params']['day'] = 'Invalid value.'
        else:
            errors['query_params']['day'] = "You must set 'day' parameter."
        if 'year' in errors['query_params'] \
            or 'month' in errors['query_params'] \
            or 'day' in errors['query_params']:
            raise ValidationError(errors)

    def list_by_priority(self, request, *args, **kwargs):
        group = self._get_group_instance(group_pk=kwargs['group_id'])
        page = self.paginate_queryset(
                                self._get_queryset_active_group_tasks(group))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list_by_date(self, request, *args, **kwargs):
        group = self._get_group_instance(group_pk=kwargs['group_id'])
        queryset = self._get_queryset_active_group_tasks(group)
        year = None if 'year' not in kwargs else int(kwargs['year'])
        month = None if 'month' not in kwargs else int(kwargs['month'])
        day = None if 'day' not in kwargs else int(kwargs['day'])
        if year is not None:
            queryset = queryset.filter(created__year=year)
        if month is not None:
            queryset = queryset.filter(created__month=month)
        if day is not None:
            queryset = queryset.filter(created__day=day)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list_completed_tasks(self, request, *args, **kwargs):
        self._query_params_validate(request.query_params)
        group = self._get_group_instance(group_pk=self.kwargs['group_id'])
        member_card = get_object_or_404(
                                self.request.user.member_cards, group=group)
        queryset = self._get_queryset_completed_group_tasks(group).filter(
            created__year=request.query_params['year'],
            created__month=request.query_params['month'],
            created__day=request.query_params['day'],
        )
        serializer = self.completed_task_serializer_class(queryset, many=True)
        return Response(serializer.data)

    def list_completed_task_dates(self, request, *args, **kwargs):
        group = self._get_group_instance(group_pk=self.kwargs['group_id'])
        member_card = get_object_or_404(
                                self.request.user.member_cards, group=group)
        year = None if 'year' not in kwargs else int(kwargs['year'])
        month = None if 'month' not in kwargs else int(kwargs['month'])
        day = None if 'day' not in kwargs else int(kwargs['day'])
        queryset = self._get_queryset_completed_group_tasks(group)
        results = queryset.values_list('created', flat=True)
        if year is not None:
            results = [date for date in results if date.year == year]
        if month is not None:
            results = [date for date in results if date.month == month]
        if day is not None:
            results = [date for date in results if date.day == day]
        return Response(results)

    def list_active_task_dates(self, request, *args, **kwargs):
        group = self._get_group_instance(group_pk=self.kwargs['group_id'])
        member_card = get_object_or_404(
                                self.request.user.member_cards, group=group)
        year = None if 'year' not in kwargs else int(kwargs['year'])
        month = None if 'month' not in kwargs else int(kwargs['month'])
        day = None if 'day' not in kwargs else int(kwargs['day'])
        queryset = self._get_queryset_active_group_tasks(group)
        results = queryset.values_list('created', flat=True)
        if year is not None:
            results = [date for date in results if date.year == year]
        if month is not None:
            results = [date for date in results if date.month == month]
        if day is not None:
            results = [date for date in results if date.day == day]
        return Response(results)

    def select_active_tasks(self, request, *args, **kwargs):
        group = self._get_group_instance(group_pk=self.kwargs['group_id'])
        member_card = get_object_or_404(
                                self.request.user.member_cards, group=group)
        queryset = self._get_queryset_active_group_tasks(group)
        serializer = GroupTasksSelectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = GroupTaskSerializer(
            queryset.filter(pk__in=serializer.data['ids']),
            many=True,
        )
        return Response(serializer.data)


    def retrieve_active_group_task(self, request, group_id, pk):
        group = self._get_group_instance(group_id)
        active_group_task = get_object_or_404(
            self._get_queryset_active_group_tasks(group),
            pk=pk,
        )
        serializer = self.active_task_serializer_class(active_group_task)
        return Response(serializer.data)

    def update_active_group_task(self, request, group_id, pk):
        group = self._get_group_instance(group_id)
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group,
        )
        if not member_card.is_staff:
            raise PermissionDenied({
                'permission_denied': 'User is not permitted to create tasks.'
            })
        serializer = self.active_task_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_task = SharedTask.objects.create(
            creator=member_card.owner,
            text=serializer.data['text'],
        )
        group_task = get_object_or_404(
            self._get_queryset_active_group_tasks(group),
            pk=pk,
        )
        group_task.shared_task.previous = shared_task
        group_task.shared_task.save()
        group_task.shared_task = shared_task
        group_task.priority = serializer.data['priority']
        group_task.save()
        group_task.to(serializer.data['order'])
        serializer = self.active_task_serializer_class(group_task)
        return Response(serializer.data)

    def update_active_group_task_order(self, request, group_id, pk):
        group = self._get_group_instance(group_id)
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group,
        )
        if not member_card.is_staff:
            raise PermissionDenied({
                'permission_denied': 'User is not permitted to update tasks.'
            })
        serializer = GroupTaskOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_task = get_object_or_404(
            self._get_queryset_active_group_tasks(group),
            pk=pk,
        )
        if 'new_priority' in serializer.data and serializer.data['new_priority'] in (1, 2, 3, 4):
            group_task.priority = serializer.data['new_priority']
            group_task.save()
        group_task_id_before = serializer.data['task_id_before']
        if group_task_id_before != -1:
            group_task_before = get_object_or_404(
                self._get_queryset_active_group_tasks(group),
                pk=group_task_id_before,
            )
            group_task.below(group_task_before)
        else:
            group_task.top()
        serializer = self.active_task_serializer_class(group_task)
        return Response(serializer.data)

    def delete_active_group_task(self, request, group_id, pk):
        group = self._get_group_instance(group_id)
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group,
        )
        if not member_card.is_staff:
            raise PermissionDenied({
                'permission_denied': 'User is not permitted to create tasks.'
            })
        group_task = get_object_or_404(
            self._get_queryset_active_group_tasks(group),
            pk=pk,
        )
        group_task.delete()
        serializer = self.active_task_serializer_class(group_task)
        return Response(serializer.data)

    def complete_active_group_task(self, request, group_id, pk):
        group = self._get_group_instance(group_id)
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group,
        )
        group_task = GroupTask.objects.get(group=group, pk=pk)
        shared_task = group_task.shared_task
        if 'shared_task_id' in request.data:
            try:
                shared_task_id = int(request.data['shared_task_id'])
                shared_task_wrapper = shared_task
                while shared_task_wrapper.pk != shared_task_id:
                    shared_task_wrapper = shared_task.previous
                    if shared_task_wrapper is None:
                        break
                if shared_task_wrapper is not None:
                    shared_task = shared_task_wrapper
            except ValueError:
                pass
        try:
            completed_group_task = CompletedGroupTask.objects.get(
                shared_task=shared_task,
                group=group,
                owner=self.request.user,
            )
            completed_group_task.priority = group_task.priority
            completed_group_task.save()
        except CompletedGroupTask.DoesNotExist:
            completed_group_task = CompletedGroupTask.objects.create(
                shared_task=shared_task,
                group=group,
                owner=self.request.user,
                priority=group_task.priority,
            )
        serializer = self.completed_task_serializer_class(completed_group_task)
        return Response(serializer.data)

    def retrieve_completed_group_task(self, request, group_id, pk):
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group_id,
        )
        completed_group_task = get_object_or_404(
            self._get_queryset_completed_group_tasks(group_id),
            pk=pk,
        )
        serializer = self.completed_task_serializer_class(completed_group_task)
        return Response(serializer.data)

    def delete_completed_group_task(self, request, group_id, pk):
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group_id,
        )
        completed_group_task = get_object_or_404(
            self._get_queryset_completed_group_tasks(group_id),
            pk=pk,
        )
        completed_group_task.delete()
        serializer = self.completed_task_serializer_class(completed_group_task)
        return Response(serializer.data)

    def create_group_task(self, request, group_id):
        group = self._get_group_instance(group_id)
        member_card = get_object_or_404(
            self.request.user.member_cards,
            group=group,
        )
        if not member_card.is_staff:
            raise PermissionDenied({
                'permission_denied': 'User is not permitted to create tasks.'
            })
        serializer = self.active_task_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_task = SharedTask.objects.create(
            creator=member_card.owner,
            text=serializer.data['text'],
        )
        group_task = GroupTask.objects.create(
            shared_task=shared_task,
            group=group,
            priority=serializer.data['priority'],
        )
        group_task.to(serializer.data['order'])
        serializer = self.active_task_serializer_class(group_task)
        return Response(serializer.data)
