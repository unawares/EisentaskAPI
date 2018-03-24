import base64
from django.db import models
from django.contrib.auth import get_user_model
from ordered_model.models import OrderedModel
from .strings import LABEL_PRIVATE, LABEL_PROTECTED, LABEL_PUBLIC
from .strings import LABEL_GOALS, LABEL_PROGRESS, LABEL_ACTIVITIES, LABEL_INTERRUPTIONS

# Create your models here.

class Assignment(models.Model):
    ACCESS_CHOICES = (
        (1, LABEL_PRIVATE),
        (2, LABEL_PROTECTED),
        (3, LABEL_PUBLIC),
    )
    uuid = models.CharField(max_length=32)
    creator = models.ForeignKey(get_user_model(),
                                related_name='assignments',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    access = models.IntegerField(choices=ACCESS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    _key = models.TextField(db_column='key')
    def key():
        def fget(self):
            return base64.decodestring(str.encode(self._key, 'utf-8'))
        def fset(self, key):
            self._key = base64.encodestring(key).decode('utf-8')
        return locals()
    key = property(**key())

    class Meta:
        ordering = ('created', 'updated',)


class AssignmentTask(OrderedModel):
    PRIORITY_CHOICES = (
        (1, LABEL_GOALS),
        (2, LABEL_PROGRESS),
        (3, LABEL_ACTIVITIES),
        (4, LABEL_INTERRUPTIONS),
    )
    text = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(OrderedModel.Meta):
        pass


class AssignmentList(models.Model):
    assignment = models.ForeignKey(Assignment,
                                    related_name='assignment_lists',
                                    on_delete=models.CASCADE)
    assignment_tasks = models.ManyToManyField(AssignmentTask,
                                              related_name='assignment_lists')
    next_list = models.OneToOneField('self',
                                     related_name='previous_list',
                                     on_delete=models.CASCADE,
                                     null=True)


class AssignmentProfile(models.Model):
    email = models.EmailField()
    assignment_list = models.ForeignKey(AssignmentList,
                                        related_name='assignment_profiles',
                                        on_delete=models.CASCADE)


class CompletedAssignmentTask(OrderedModel):
    profile = models.ForeignKey(AssignmentProfile,
                                related_name='completed_assignment_tasks',
                                on_delete=models.CASCADE)
    assignment_task = models.ForeignKey(AssignmentTask,
                                        related_name='completed_assignment_tasks',
                                        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class ArchivedAssignmentTask(OrderedModel):
    profile = models.ForeignKey(AssignmentProfile,
                                related_name='archived_assignment_tasks',
                                on_delete=models.CASCADE)
    assignment_task = models.ForeignKey(AssignmentTask,
                                        related_name='archived_assignment_tasks',
                                        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
