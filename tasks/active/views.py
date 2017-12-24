from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ActiveTasksSerializer
from .serializers import OrderedTaskSerializer, OrderedTasksSerializer
from .models import ActiveTasks
from tasks.models import Task

# Create your views here.

class ActiveTasksView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        active_tasks, created = ActiveTasks.objects \
                                        .get_or_create(owner=request.user)
        serializer = OrderedTasksSerializer({
            'tasks': Task.objects.filter(owner=request.user),
            'active_tasks': active_tasks,
        })
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderedTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
