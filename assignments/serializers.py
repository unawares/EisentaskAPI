from rest_framework import serializers
from assignments.protected.models import AssignmentInfo
from .models import Assignment
from .models import AssignmentList
from .models import AssignmentTask
from .models import AssignmentProfile


class AssignmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentInfo
        fields = ('assignment_info',)


class AssignmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentTask
        fields = ('id', 'text', 'priority', 'created', 'updated',)


class AssignmentSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_my_info')
    def get_my_info(self, obj):
        info = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            assignment_profile = None
            try:
                assignment_profile = AssignmentProfile.objects.filter(
                    assignment_list__in=obj.assignment_lists.values_list('id')
                ).get(email=user.email)
                info = AssignmentInfoSerializer(AssignmentInfo.objects.get(
                    assignment_profile=assignment_profile,
                    email=user.email
                )).data
            except AssignmentProfile.DoesNotExist:
                pass
            except AssignmentInfo.DoesNotExist:
                pass
        return info
    class Meta:
        model = Assignment
        fields = ('creator', 'name', 'description', 'access', 'uuid', 'archived', 'label_color', 'info',)
        read_only_fields = ('creator', 'uuid',)


class AssignmentListSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    assignment_tasks = AssignmentTaskSerializer(read_only=True, many=True)
    class Meta:
        model = AssignmentList
        fields = ('assignment', 'assignment_tasks', 'next_list', 'orders',)
        read_only_fields = ('assignment', 'assignment_tasks', 'next_list', 'orders',)
