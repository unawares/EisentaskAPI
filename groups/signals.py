from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Group
from .models import MemberCard

@receiver(post_save, sender=Group)
def create_member_card(sender, instance, created, **kwargs):
    if created:
        MemberCard.objects.create(group=instance,
                                  owner=instance.admin,
                                  is_staff=True)
