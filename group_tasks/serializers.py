from rest_framework import serializers
from .models import SharedTask
from .models import GroupTask


class SharedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTask
        fields = '__all__'

class GroupTaskSerializer(serializers.ModelSerializer):
    shared_task = SharedTaskSerializer(read_only=True)
    class Meta:
        model = GroupTask
        fields = '__all__'
