from django.db import models
from django.contrib.auth import get_user_model
from ordered_model.models import OrderedModel
from groups.models import Group
from .strings import LABEL_GOALS, LABEL_PROGRESS, LABEL_ACTIVITIES, LABEL_INTERRUPTIONS


# Create your models here.

PRIORITY_CHOICES = (
    (1, LABEL_GOALS),
    (2, LABEL_PROGRESS),
    (3, LABEL_ACTIVITIES),
    (4, LABEL_INTERRUPTIONS),
)

class SharedTask(models.Model):
    creator = models.ForeignKey(get_user_model(),
                                related_name='shared_tasks',
                                on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(get_user_model(), related_name='likes')
    dislikes = models.ManyToManyField(get_user_model(), related_name='dislikes')
    previous = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)


class GroupTask(OrderedModel):
    shared_task = models.ForeignKey(SharedTask,
                                    related_name='group_tasks',
                                    on_delete=models.CASCADE)
    group = models.ForeignKey(Group,
                              related_name='group_tasks',
                              on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    order_with_respect_to = 'group'


    class Meta(OrderedModel.Meta):
        pass


class CompletedGroupTask(models.Model):
    owner = models.ForeignKey(get_user_model(),
                              related_name='completed_group_tasks',
                              on_delete=models.CASCADE)
    shared_task = models.ForeignKey(SharedTask,
                                    related_name='completed_group_tasks',
                                    on_delete=models.CASCADE)
    group = models.ForeignKey(Group,
                              related_name='completed_group_tasks',
                              on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
