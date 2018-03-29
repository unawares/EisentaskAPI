import base64
from enum import Enum
from uuid import uuid4
from cryptography.fernet import Fernet
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from assignments.models import Assignment
from assignments.models import AssignmentList
from assignments.models import AssignmentTask
from .exceptions import AssignmentActionsError


class AssignmentActions:
    class ActionTypes(Enum):
        CREATE = 'create'
        UPDATE = 'update'
        DELETE = 'delete'
        NONE = 'none'

    @staticmethod
    def new_assignment(creator, name, description, label_color, access=1):
        assignment = Assignment(uuid=uuid4().hex,
                                creator=creator,
                                name=name,
                                description=description,
                                label_color=label_color,
                                access=access)
        assignment.key = Fernet.generate_key()
        assignment.save()
        return assignment

    class Actions:
        def __init__(self, user, assignment):
            self.user = user
            self.assignment = assignment
            assignment_list = None
            try:
                assignment_list = assignment.assignment_lists.get(next_list=None)
            except AssignmentList.DoesNotExist:
                pass
            if assignment_list and assignment != assignment_list.assignment:
                raise AssignmentActionsError('User does not have access.')
            self.assignment_list = assignment_list

        def override(self, tasks):
            assignment_list = AssignmentList.objects.create(assignment=self.assignment)
            if self.assignment_list:
                assignment_list.assignment_tasks.add(*self.assignment_list.assignment_tasks.all())
            for task in tasks:
                try:
                    if task['action'] == AssignmentActions.ActionTypes.CREATE.value:
                        assignment_list.assignment_tasks.add(
                            AssignmentTask.objects.create(
                                text=task['text'],
                                priority=task['priority']
                            )
                        )
                    elif task['action']  == AssignmentActions.ActionTypes.UPDATE.value:
                        assignment_task = self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        assignment_list.assignment_tasks.remove(assignment_task)
                        if len(assignment_task.assignment_lists.all()) == 0:
                            assignment_task.delete()
                        assignment_list.assignment_tasks.add(
                            AssignmentTask.objects.create(
                                text=task['text'],
                                priority=task['priority']
                            )
                        )
                    elif task['action']  == AssignmentActions.ActionTypes.DELETE.value:
                        assignment_task = self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        assignment_list.assignment_tasks.remove(assignment_task)
                        if len(assignment_task.assignment_lists.all()) == 0:
                            assignment_task.delete()
                        continue
                    elif task['action']  == AssignmentActions.ActionTypes.NONE.value:
                        assignment_list.assignment_tasks.add(
                            self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        )
                except AssignmentTask.DoesNotExist:
                    pass
            assignment_list.save()
            if self.assignment_list and len(self.assignment_list.assignment_profiles.all()) == 0:
                try:
                    previous_list = self.assignment_list.previous_list
                    previous_list.next_list = assignment_task
                    previous_list.save()
                except ObjectDoesNotExist:
                    self.assignment_list.delete()
                    self.assignment_list = assignment_list
            elif self.assignment_list:
                self.assignment_list.next_list = assignment_list
                self.assignment_list.save()
            else:
                self.assignment_list = assignment_list

        def get_assignment_list(self):
            return self.assignment_list

    def __init__(self, user, assignment):
        if user != assignment.creator:
            raise AssignmentActionsError('User does not have access.')
        self.user = user
        self.assignment = assignment

    def __enter__(self):
        return AssignmentActions.Actions(self.user, self.assignment)

    def __exit__(self, type, value, traceback):
        pass
