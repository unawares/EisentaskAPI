from rest_framework import serializers
from .models import ActiveTasks

class ActiveTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveTasks
        fields = '__all__'
        read_only_fields = ('owner',)
