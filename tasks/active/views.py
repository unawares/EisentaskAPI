from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import ActiveTasksSerializer
from .models import ActiveTasks

# Create your views here.

class ActiveTasksViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveTasksSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get',)

    def get_queryset(self):
        return ActiveTasks.objects.filter(owner=self.request.user)
