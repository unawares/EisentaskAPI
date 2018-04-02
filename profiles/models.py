from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Profile(models.Model):
    owner = models.OneToOneField(get_user_model(),
                                 related_name='profile',
                                 on_delete=models.CASCADE)
    data = JSONField(default={})
