from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Group(models.Model):
    admin = models.ForeignKey(get_user_model(),
                                related_name='created_groups',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    is_joining_allowed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='group_images/%Y/%m/%d', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class MemberCard(models.Model):
    group = models.ForeignKey(Group,
                              related_name='member_cards',
                              on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(),
                              related_name='member_cards',
                              on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
