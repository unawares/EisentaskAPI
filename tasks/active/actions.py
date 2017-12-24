from .models import ActiveTasks

# Active tasks actions

class ActiveTasksActions:
    class PositionException(Exception):
        pass

    def __init__(self, instance):  # Takes task instance
        self.instance = instance
        self.active_tasks = ActiveTasks.objects.get(owner=instance.owner)
        self.preferences = {
            1: self.active_tasks.goals,
            2: self.active_tasks.progress,
            3: self.active_tasks.activities,
            4: self.active_tasks.interruptions,
        }

    def to_positon(self, pos):
        if pos < 0 or pos >= len(self.preferences[self.instance.priority]):
            raise self.PositionException("New position is incorrect.")
        self.preferences[self.instance.priority].remove(self.instance.pk)
        self.preferences[self.instance.priority].insert(pos, self.instance.pk)
        return self

    def commit_and_get_active_tasks_instance(self):
        self.commit()
        return self.active_tasks

    def commit(self):
        self.active_tasks.save()

    def next_position(self):
        return len(self.preferences[self.instance.priority])

    def get_active_tasks(self):
        return self.active_tasks

    def get_position(self):
        return self.preferences[self.instance.priority].index(self.instance.pk)
