from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from assignments.models import AssignmentList
from assignments.serializers import AssignmentSerializer
from assignments.serializers import AssignmentListSerializer
from .serializers import TasksSerializer
from .actions import AssignmentActions

# Create your views here.
class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f]{32}'

    def get_queryset(self):
        return self.request.user.assignments.all()

    @list_route(methods=['post'], serializer_class=TasksSerializer)
    def create_assignment_tasks(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment_list = None
        with AssignmentActions(
            request.user,
            AssignmentActions.new_assignment(
                creator=request.user,
                name=serializer.data['name'],
                description=serializer.data['description']
            )
        ) as manager:
            manager.override(serializer.data['tasks'])
            assignment_list = manager.get_assignment_list()
        return Response(AssignmentListSerializer(assignment_list).data)

    @detail_route(methods=['get'], serializer_class=TasksSerializer)
    def get_assignment_tasks(self, request, *args, **kwargs):
        assignment = self.get_object()
        assignment_list = get_object_or_404(assignment.assignment_lists, next_list=None)
        return Response(AssignmentListSerializer(assignment_list).data)

    @detail_route(methods=['put'], serializer_class=TasksSerializer)
    def update_assignment_tasks(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment_list = None
        assignment = self.get_object()
        if 'name' in serializer.data:
            assignment.name = serializer.data['name']
        if 'description' in serializer.data:
            assignment.description = serializer.data['description']
        assignment.save()
        with AssignmentActions(request.user, assignment) as manager:
            manager.override(serializer.data['tasks'])
            assignment_list = manager.get_assignment_list()
        return Response(AssignmentListSerializer(assignment_list).data)

    @detail_route(methods=['delete'], serializer_class=TasksSerializer)
    def delete_assignment_tasks(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment_list = None
        assignment = self.get_object()
        assignment.delete()
        return Response(AssignmentListSerializer(assignment_list).data)
