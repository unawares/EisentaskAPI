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


class OrderedTasksSerializer(serializers.Serializer):
    """
    This is used to get list of tasks with their orders

    """
    tasks = TaskSerializer(many=True)
    active_tasks = ActiveTasksSerializer(read_only=True)


class OrderedTaskSerializer(serializers.Serializer):
    """
    This is used to create, update a taks
    Custom create and update methods are required because of nested serializers


    """
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

    def update(self, instance, validated_data):
        task = instance['task']
        task.text = validated_data['task'].get('text', task.text)
        task.priority = validated_data['task'].get('priority', task.priority)
        task.completed = validated_data['task'].get('completed', task.completed)
        task.save()
        actions = ActiveTasksActions(task, instance.get('active_tasks', None))
        instance['active_tasks'] = actions.get_active_tasks()
        if not task.completed:
            if 'new_position' in validated_data:
                last_pos = actions.next_position() - 1
                new_position = validated_data['new_position']
                if (new_position >= 0 and new_position <= last_pos):
                    instance['active_tasks'] = actions.to_positon(new_position) \
                                                      .commit_and_get_active_tasks_instance()
                    instance['new_position'] = new_position
        return instance
