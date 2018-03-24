from rest_framework import serializers
from .validators import TasksFormatValidator
from assignments.models import Assignment

class TasksSerializer(serializers.Serializer):
    tasks = serializers.ListField(
        child=serializers.JSONField(),
        validators=[TasksFormatValidator()]
    )
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
