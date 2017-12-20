from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ActiveTasks
from tasks.models import Task


# On task create, update and delete signals

@receiver(post_save, sender=Task)
def update_active_tasks_orders_on_create(sender, instance, created, **kwargs):
    if created and not instance.completed:
        active_tasks = ActiveTasks.objects.get(owner=instance.owner)
        preferences = {
            1: active_tasks.goals,
            2: active_tasks.progress,
            3: active_tasks.activities,
            4: active_tasks.interruptions,
        }
        preferences[instance.priority].append(instance.pk)
        active_tasks.save()


@receiver(pre_save, sender=Task)
def update_active_tasks_orders_on_change(sender, instance, **kwargs):
    task = None
    try:
        task = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    if task:  # If a task is going to be updated
        active_tasks = ActiveTasks.objects.get(owner=instance.owner)
        preferences = {
            1: active_tasks.goals,
            2: active_tasks.progress,
            3: active_tasks.activities,
            4: active_tasks.interruptions,
        }
        if instance.completed:  # If a task is going to be completed
                                # then remove it from orders
            if task.pk in preferences[task.priority]:  # We check by old state
                                                       # because the priority may be changed
                preferences[task.priority].remove(task.pk)
        elif instance.priority != task.priority:  # If the priority of a task is changed,
                                                  # then delete its order depended to the old priority
            if task.pk in preferences[task.priority]:
                preferences[task.priority].remove(task.pk)
            preferences[instance.priority].append(instance.pk)
        elif not instance.completed:
            if instance.pk not in preferences[instance.priority]:
                preferences[instance.priority].append(instance.pk)
        active_tasks.save()


@receiver(post_delete, sender=Task)
def update_active_tasks_orders_on_delete(sender, instance, **kwargs):
    if not instance.completed: # If task is not completed, then delete its order as well
        active_tasks = ActiveTasks.objects.get(owner=instance.owner)
        preferences = {
            1: active_tasks.goals,
            2: active_tasks.progress,
            3: active_tasks.activities,
            4: active_tasks.interruptions,
        }
        if instance.pk in preferences[instance.priority]:
            preferences[instance.priority].remove(instance.pk)
        active_tasks.save()
