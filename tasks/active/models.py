from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

# Create your models here.

class ActiveTasks(models.Model):
    owner = models.OneToOneField(get_user_model(),
                                 related_name='active_tasks',
                                 on_delete=models.CASCADE)
    goals = JSONField(default=[])  # Orders of tasks with 1 priority
    progress = JSONField(default=[])  # Orders of tasks with 2 priority
    activities = JSONField(default=[])  # Orders of tasks with 3 priority
    interruptions = JSONField(default=[])  # Orders of tasks with 4 priority
