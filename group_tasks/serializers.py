from rest_framework import serializers
from .models import SharedTask
from .models import GroupTask
from .models import CompletedGroupTask


class SharedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTask
        fields = '__all__'

class GroupTaskSerializer(serializers.ModelSerializer):
    shared_task = SharedTaskSerializer(read_only=True)
    class Meta:
        model = GroupTask
        fields = '__all__'

class CompletedGroupTaskSerializer(serializers.ModelSerializer):
    shared_task = SharedTaskSerializer(read_only=True)
    class Meta:
        model = CompletedGroupTask
        fields = '__all__'
        read_only_fields = ('created', 'updated', 'owner',
                            'group', 'priority', 'shared_task')
