from rest_framework import serializers
from .models import ActiveTasks
from tasks.serializers import TaskSerializer
from tasks.models import Task
from .actions import ActiveTasksActions
from django.db import IntegrityError

# Serializers

class ActiveTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveTasks
        exclude = ('id', 'owner',)


class OrderedTaskSerializer(serializers.Serializer):
    new_position = serializers.IntegerField(required=False)
    task = TaskSerializer()
    active_tasks = ActiveTasksSerializer(read_only=True)

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        task = Task.objects.create(**validated_data['task'], owner=user)
        actions = ActiveTasksActions(task)
        active_tasks = actions.get_active_tasks()
        if 'new_position' in validated_data:
            last_pos = actions.next_position() - 1
            new_position = validated_data['new_position']
            if (new_position >= 0 and new_position <= last_pos):
                active_tasks = actions.to_positon(new_position) \
                                      .commit_and_get_active_tasks_instance()
        return {
            'new_position': actions.get_position(),
            'task': task,
            'active_tasks': active_tasks,
        }


class OrderedTasksSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)
    active_tasks = ActiveTasksSerializer(read_only=True)
