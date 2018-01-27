from django.db import models
from django.contrib.auth import get_user_model
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
    previous = models.ForeignKey('self', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class GroupTask(models.Model):
    shared_task = models.ForeignKey(SharedTask,
                                    related_name='group_tasks',
                                    on_delete=models.CASCADE)
    group = models.ForeignKey(Group,
                              related_name='group_tasks',
                              on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
