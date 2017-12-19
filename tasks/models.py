from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from .strings import LABEL_GOALS, LABEL_PROGRESS, LABEL_ACTIVITIES, LABEL_INTERRUPTIONS

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = (
        (1, LABEL_GOALS),
        (2, LABEL_PROGRESS),
        (3, LABEL_ACTIVITIES),
        (4, LABEL_INTERRUPTIONS),
    )

    owner = models.ForeignKey(get_user_model(),
                              related_name='tasks',
                              on_delete=models.CASCADE,)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
