from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ActiveTasksSerializer
from .models import ActiveTasks

# Create your views here.

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def active_tasks_view(request):
    active_tasks, created = ActiveTasks.objects.get_or_create(owner=request.user)
    serializers = ActiveTasksSerializer(active_tasks)
    return Response(serializers.data)
