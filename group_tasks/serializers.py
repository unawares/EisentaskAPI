from rest_framework import serializers
from .models import SharedTask
from .models import GroupTask
from .models import CompletedGroupTask


class SharedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTask
        fields = '__all__'


class GroupTaskSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='shared_task.text')
    order = serializers.IntegerField(default=0)
    class Meta:
        model = GroupTask
        exclude = ('shared_task', 'group',)


class CompletedGroupTaskSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='shared_task.text')
    class Meta:
        model = CompletedGroupTask
        exclude = ('shared_task', 'group', 'owner',)
        read_only_fields = ('created', 'updated', 'priority',)
