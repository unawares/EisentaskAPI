from rest_framework import serializers
from .actions import AssignmentActions

action_types = (
    AssignmentActions.ActionTypes.CREATE.value,
    AssignmentActions.ActionTypes.UPDATE.value,
    AssignmentActions.ActionTypes.DELETE.value,
    AssignmentActions.ActionTypes.NONE.value,
)

class TasksFormatValidator(object):
    def __call__(self, tasks):
        if len(tasks) == 0:
            raise serializers.ValidationError('Blank is not allowed')
        for task in tasks:
            if type(task) is not dict:
                raise serializers.ValidationError('Instances must be a dict.')
            elif 'action' not in task:
                raise serializers.ValidationError("Instances must have 'action' property.")
            elif task['action'] not in action_types:
                raise serializers.ValidationError(
                    "'action' property must be one of %s/%s/%s/%s." % action_types
                )
            elif task['action'] == action_types[0]:
                if 'text' not in task or type(task['text']) is not str:
                    raise serializers.ValidationError("'text' property must be set and must be string type.")
                if 'priority' not in task or type(task['priority']) is not int:
                    raise serializers.ValidationError("'priority' property must be set and must be integer type.")
                if task['priority'] not in range(1, 5):
                    raise serializers.ValidationError("'priority' property must be in range 1-4.")
            elif task['action'] == action_types[1]:
                if 'pk' not in task or type(task['pk']) is not int:
                    raise serializers.ValidationError("'pk' property must be set and must be integer type.")
                if 'text' not in task or type(task['text']) is not str:
                    raise serializers.ValidationError("'text' property must be set and must be string type.")
                if 'priority' not in task or type(task['priority']) is not int:
                    raise serializers.ValidationError("'priority' property must be set and must be integer type.")
                if task['priority'] not in range(1, 5):
                    raise serializers.ValidationError("'priority' property must be in range 1-4.")
            elif task['action'] == action_types[2]:
                if 'pk' not in task or type(task['pk']) is not int:
                    raise serializers.ValidationError("'pk' property must be set and must be integer type.")
            elif task['action'] == action_types[3]:
                if 'pk' not in task or type(task['pk']) is not int:
                    raise serializers.ValidationError("'pk' property must be set and must be integer type.")


class TaskLabelColorRangeValidator(object):
    def __call__(self, label_color):
        if label_color < 1 or label_color > 4:
            raise serializers.ValidationError('The value of label color must be one of the values: 1, 2, 3, 4.')
