from .models import ActiveTasks

# Active tasks actions

class ActiveTasksActions:
    """
    Actions tasks controls the tasks' orders

    """
    class PositionException(Exception):
        """
        Exception class is raised when an incorrect position

        """
        pass

    def __init__(self, instance, active_tasks=None):  # Takes task instance
        """
        Constructor: takes one argument if task instance
        Retrives active tasks instance from given task

        """
        if active_tasks is None:
            active_tasks = ActiveTasks.objects.get(owner=instance.owner)
        else:
            active_tasks.refresh_from_db()
        self.instance = instance
        self.active_tasks = active_tasks
        self.preferences = {
            1: self.active_tasks.goals,
            2: self.active_tasks.progress,
            3: self.active_tasks.activities,
            4: self.active_tasks.interruptions,
        }

    def to_positon(self, pos):
        """
        Move the task to given position

        """
        if pos < 0 or pos >= len(self.preferences[self.instance.priority]):
            raise self.PositionException("New position is incorrect.")
        self.preferences[self.instance.priority].remove(self.instance.pk)
        self.preferences[self.instance.priority].insert(pos, self.instance.pk)
        return self

    def commit_and_get_active_tasks_instance(self):
        """
        Commit changes and return task instance

        """
        self.commit()
        return self.active_tasks

    def commit(self):
        """
        Commit changes

        """
        self.active_tasks.save()

    def next_position(self):
        """
        Get next position from the priorities of given task

        """
        return len(self.preferences[self.instance.priority])

    def get_active_tasks(self):
        """
        Get active tasks instance

        """
        return self.active_tasks

    def get_position(self):
        """
        Get the position of given task from the priorities of it

        """
        return self.preferences[self.instance.priority].index(self.instance.pk)
