import base64
from enum import Enum
from uuid import uuid4
from cryptography.fernet import Fernet
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from assignments.models import Assignment
from assignments.models import AssignmentList
from assignments.models import AssignmentTask
from assignments.models import AssignmentProfile
from .exceptions import AssignmentActionsError


class AssignmentActions:
    class ActionTypes(Enum):
        CREATE = 'create'
        UPDATE = 'update'
        DELETE = 'delete'
        NONE = 'none'

    @staticmethod
    def new_assignment(creator, name, description, label_color, access=2):
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
            order = 1
            orders = {}
            users = None
            assignment_list = AssignmentList.objects.create(assignment=self.assignment)
            if self.assignment_list:
                users = self.assignment_list.assignment_profiles.all()
            for task in tasks:
                try:
                    if task['action'] == AssignmentActions.ActionTypes.CREATE.value:
                        assignment_task = AssignmentTask.objects.create(
                            text=task['text'],
                            priority=task['priority']
                        )
                        assignment_list.assignment_tasks.add(assignment_task)
                        orders[assignment_task.pk] = order
                        order += 1
                    elif task['action']  == AssignmentActions.ActionTypes.UPDATE.value:
                        t = self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        list_ids = t.assignment_lists.values_list('id', flat=True)
                        profiles = AssignmentProfile.objects.filter(assignment_list__in=list_ids)
                        if users is not None and len(profiles) == 0:
                            t.delete()
                        assignment_task = None
                        if t.text == task['text'] and t.priority == task['priority']:
                            assignment_task = t
                        else:
                            assignment_task = AssignmentTask.objects.create(
                                text=task['text'],
                                priority=task['priority']
                            )
                        assignment_list.assignment_tasks.add(assignment_task)
                        orders[assignment_task.pk] = order
                        order += 1
                    elif task['action']  == AssignmentActions.ActionTypes.DELETE.value:
                        t = self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        list_ids = t.assignment_lists.values_list('id', flat=True)
                        profiles = AssignmentProfile.objects.filter(assignment_list__in=list_ids)
                        if users is not None and len(profiles) == 0:
                            t.delete()
                    elif task['action']  == AssignmentActions.ActionTypes.NONE.value:
                        if users is None:
                            continue
                        assignment_task = self.assignment_list.assignment_tasks.get(pk=task['pk'])
                        assignment_list.assignment_tasks.add(assignment_task)
                        orders[assignment_task.pk] = order
                        order += 1
                except AssignmentTask.DoesNotExist:
                    pass
            assignment_list.orders = orders
            assignment_list.save()
            if users is not None and len(users) == 0:
                try:
                    previous_list = self.assignment_list.previous_list
                    previous_list.next_list = assignment_list
                    previous_list.save()
                except ObjectDoesNotExist:
                    pass
                finally:
                    self.assignment_list.delete()
            elif users is not None:
                self.assignment_list.next_list = assignment_list
                self.assignment_list.save()
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
