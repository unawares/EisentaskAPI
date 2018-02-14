from rest_framework import serializers
from .models import SharedTask
from .models import GroupTask
from .models import CompletedGroupTask
from .models import PRIORITY_CHOICES


class SharedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTask
        fields = '__all__'


class GroupTaskSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='shared_task.text')
    order = serializers.IntegerField(default=0)
    class Meta:
        model = GroupTask
        exclude = ('group', 'shared_task',)
        read_only_fields = ('created', 'updated',)


class CompletedGroupTaskSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='shared_task.text')
    class Meta:
        model = CompletedGroupTask
        exclude = ('group', 'owner', 'shared_task',)
        read_only_fields = ('created', 'updated', 'priority',)


class GroupTaskOrderSerializer(serializers.Serializer):
    task_id_before = serializers.IntegerField(default=-1)
    new_priority = serializers.IntegerField(required=False)


class GroupTasksSelectionSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child = serializers.IntegerField()
    )
