from assignments.models import AssignmentTask
from assignments.models import CompletedAssignmentTask
from assignments.models import ArchivedAssignmentTask

class AssignmentTaskActions:
    class Actions:
        def __init__(self, assignment, assignment_info):
            self.assignment = assignment
            self.assignment_info = assignment_info

        def complete_task(self, task):
            completed_task, created = CompletedAssignmentTask.objects.get_or_create(
                profile=self.assignment_info.assignment_profile,
                assignment_task=task
            )
            pass

        def cancel_task(self, task):
            CompletedAssignmentTask.objects.filter(
                profile=self.assignment_info.assignment_profile,
                assignment_task=task
            ).delete()
            pass

        def archive_task(self, task):
            archived_task, created = ArchivedAssignmentTask.objects.get_or_create(
                profile=self.assignment_info.assignment_profile,
                assignment_task=task
            )
            pass

    def __init__(self, assignment, assignment_info):
        self.assignment = assignment
        self.assignment_info = assignment_info

    def __enter__(self):
        return AssignmentTaskActions.Actions(self.assignment, self.assignment_info)

    def __exit__(self, type, value, traceback):
        pass
