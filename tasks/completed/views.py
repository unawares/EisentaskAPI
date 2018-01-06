from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from tasks.serializers import TaskSerializer

# Create your views here.

class CompletedTasksView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = TaskSerializer(
            Task.objects.filter(owner=request.user, completed=True),
            many=True)
        return Response(serializer.data)


class CompletedTasksDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=True)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=True)
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user, completed=True)
        task.delete()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
