from rest_framework import serializers
from assignments.models import Assignment
from assignments.models import AssignmentProfile
from .validators import TasksFormatValidator
from .validators import TaskLabelColorRangeValidator

class TasksSerializer(serializers.Serializer):
    tasks = serializers.ListField(
        child=serializers.JSONField(),
        validators=[TasksFormatValidator()]
    )
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    label_color = serializers.IntegerField(
        validators=[TaskLabelColorRangeValidator()]
    )


class UpdateTasksSerializer(serializers.Serializer):
    tasks = serializers.ListField(
        child=serializers.JSONField(),
        validators=[TasksFormatValidator()],
        required=False
    )
    name = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    label_color = serializers.IntegerField(
        required=False,
        validators=[TaskLabelColorRangeValidator()]
    )


class AssignmentProfileEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentProfile
        fields = ('email',)
        read_only_fields = ('email',)
