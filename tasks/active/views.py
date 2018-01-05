from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ActiveTasksSerializer
from .serializers import OrderedTaskSerializer, OrderedTasksSerializer
from .models import ActiveTasks
from tasks.models import Task

# Create your views here.

class ActiveTasksView(APIView):
    """
    List view
    Get and post methods are allowed

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get active tasks with the orders

        """
        active_tasks, created = ActiveTasks.objects \
                                        .get_or_create(owner=request.user)
        serializer = OrderedTasksSerializer({
            'tasks': Task.objects.filter(owner=request.user, completed=False),
            'active_tasks': active_tasks,
        })
        return Response(serializer.data)

    def post(self, request):
        """
        Create task with it's order and return changed orders

        """
        serializer = OrderedTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class ActiveTasksDetailView(APIView):
    """
    Detail view
    Get, put and delete methods are allowed

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=False)
        active_tasks = ActiveTasks.objects.get(owner=request.user)
        serializer = OrderedTaskSerializer({
            'task': task,
            'active_tasks': active_tasks,
        })
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=False)
        active_tasks = ActiveTasks.objects.get(owner=request.user)
        serializer = OrderedTaskSerializer({
            'task': task,
            'active_tasks': active_tasks,
        }, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=False)
        task.delete()
        active_tasks = ActiveTasks.objects.get(owner=request.user)
        serializer = OrderedTaskSerializer({
            'task': task,
            'active_tasks': active_tasks,
        })
        return Response(serializer.data)
