from django.db import models
from django.contrib.auth import get_user_model
from ordered_model.models import OrderedModel
from .strings import LABEL_PRIVATE, LABEL_PROTECTED, LABEL_PUBLIC
from .strings import LABEL_GOALS, LABEL_PROGRESS, LABEL_ACTIVITIES, LABEL_INTERRUPTIONS

# Create your models here.

ACCESS_CHOICES = (
    (1, LABEL_PRIVATE),
    (2, LABEL_PROTECTED),
    (3, LABEL_PUBLIC),
)

PRIORITY_CHOICES = (
    (1, LABEL_GOALS),
    (2, LABEL_PROGRESS),
    (3, LABEL_ACTIVITIES),
    (4, LABEL_INTERRUPTIONS),
)

STATE_CHOICES = (
    (1, LABEL_ACTIVE),
    (2, LABEL_COMPLETED),
    (3, LABEL_DELETED),
)

class Assignments(models.Model):
    uuid = models.CharField(max_length=32)
    creator = models.ForeignKey(get_user_model(),
                                related_name='assignments',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    access = models.IntegerField(choices=ACCESS_CHOICES)
    _key = models.TextField(db_column='key')
    def key():
        def fget(self):
            return base64.decodestring(self._key)
        def fset(self, value):
            self._key = base64.encodestring(key)
        return locals()
    key = property(**key())


class AssignmentTasks(models.Model):
    assignments = models.ForeignKey(Assignments,
                                    related_name='assignment_tasks'
                                    on_delete=models.CASCADE)
    uuid = models.CharField(max_length=32)
    goals = JSONField(default=[])
    progress = JSONField(default=[])
    activities = JSONField(default=[])
    interruptions = JSONField(default=[])
    previous_tasks = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    next_tasks = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


"""
class AssignmentProfile(models.Model):
    assignment_tasks = models.ForeignKey(AssignmentTasks,
                                         related_name='assignment_profiles'
                                         on_delete=models.CASCADE)
    email = models.EmailField(max_length=70)
    uuid = models.CharField(max_length=32)
    _key = models.TextField(db_column='key')

    def key():
        def fget(self):
            return base64.decodestring(self._key)
        def fset(self, value):
            self._key = base64.encodestring(key)
        return locals()
    key = property(**key())
"""
