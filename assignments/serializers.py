from rest_framework import serializers
from .models import Assignment
from .models import AssignmentList
from .models import AssignmentTask


class AssignmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentTask
        fields = ('id', 'text', 'priority', 'created', 'updated',)


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('creator', 'name', 'description', 'access', 'uuid',)
        read_only_fields = ('creator', 'uuid',)


class AssignmentListSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    assignment_tasks = AssignmentTaskSerializer(read_only=True, many=True)
    class Meta:
        model = AssignmentList
        fields = ('assignment', 'assignment_tasks', 'next_list',)
        read_only_fields = ('assignment', 'assignment_tasks', 'next_list',)
