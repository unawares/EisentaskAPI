from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import base64
import _pickle as pickle
from urllib import parse
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from assignments.models import Assignment
from assignments.models import AssignmentTask
from assignments.models import CompletedAssignmentTask
from assignments.models import ArchivedAssignmentTask
from .models import AssignmentInfo
from .actions import AssignmentTaskActions

# Create your views here.

class Utils:
    @staticmethod
    def _get_all_tasks_instance(assignment_info):
        return assignment_info.assignment_profile.assignment_list.assignment_tasks

    @staticmethod
    def _get_all_completed_tasks_instance(assignment_info):
        return assignment_info.assignment_profile.completed_assignment_tasks

    @staticmethod
    def _get_all_archived_tasks_instance(assignment_info):
        return assignment_info.assignment_profile.archived_assignment_tasks

    @staticmethod
    def get_active_tasks_instance(assignment_info):
        profile = assignment_info.assignment_profile
        archived_task_ids = Utils._get_all_archived_tasks_instance(assignment_info) \
            .values_list('assignment_task', flat=True)
        completed_task_ids = Utils._get_all_completed_tasks_instance(assignment_info) \
            .values_list('assignment_task', flat=True)
        return Utils._get_all_tasks_instance(assignment_info) \
            .exclude(id__in=archived_task_ids).exclude(id__in=completed_task_ids)

    @staticmethod
    def get_completed_tasks_instance(assignment_info):
        archived_task_ids = Utils._get_all_archived_tasks_instance(assignment_info) \
            .values_list('assignment_task', flat=True)
        complete_task_ids = Utils._get_all_completed_tasks_instance(assignment_info) \
            .exclude(assignment_task__in=archived_task_ids) \
            .values_list('assignment_task', flat=True)
        return Utils._get_all_tasks_instance(assignment_info).filter(id__in=complete_task_ids)

    @staticmethod
    def get_archived_tasks_instance(assignment_info):
        archived_task_ids = Utils._get_all_archived_tasks_instance(assignment_info) \
            .values_list('assignment_task', flat=True)
        return Utils._get_all_tasks_instance(assignment_info).filter(id__in=complete_task_ids)

    @staticmethod
    def get_assignment_instances(assignment_uuid_str, assignment_info_str):
        ACCESS_PRIVATE = 1
        ACCESS_PROTECTED = 2
        ACCESS_PUBLIC = 3
        assignment = get_object_or_404(Assignment, uuid=assignment_uuid_str)
        info = None
        assignment_info = None
        try:
            f = Fernet(assignment.key)
            b_info = f.decrypt(assignment_info_str.encode('utf-8'))
            info = pickle.loads(b_info)
        except Exception:
            raise Http404
        if type(info) is dict and 'uuid' in info:
            assignment_info = get_object_or_404(
                AssignmentInfo,
                assignment_uuid=info['uuid'],
                _assignment_info=base64.encodestring(assignment_info_str.encode('utf-8')).decode('utf-8')
            )
        if (
            assignment.access == ACCESS_PRIVATE and assignment.creator.email == assignment_info.email
        ) or (
            assignment.access != ACCESS_PRIVATE
        ):
            return assignment, assignment_info
        else:
            raise Http404



def active_tasks_view(request, uuid, info):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    active_tasks_instance = Utils.get_active_tasks_instance(assignment_info)
    orders = assignment_info.assignment_profile.assignment_list.orders
    f = lambda task: orders[str(task.pk)]
    goals = sorted(active_tasks_instance.filter(priority=1), key=f)
    progress = sorted(active_tasks_instance.filter(priority=2), key=f)
    activities = sorted(active_tasks_instance.filter(priority=3), key=f)
    interruptions = sorted(active_tasks_instance.filter(priority=4), key=f)
    return render(request, 'assignments/active_tasks.html', {
        'is_owner': assignment_info.email == assignment_info.assignment_profile.email,
        'has_next_list': assignment_info.assignment_profile.assignment_list.next_list != None,
        'assignment_info': {
            'email': assignment_info.email,
            'access': assignment_info.access,
            'uuid': assignment.uuid,
            'info': assignment_info.assignment_info.decode('utf-8')
        },
        'tasks': {
            'goals': goals,
            'progress': progress,
            'activities': activities,
            'interruptions': interruptions
        },
        'section': 'active_tasks'
    })


def completed_tasks_view(request, uuid, info):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    completed_tasks_instance = Utils.get_completed_tasks_instance(assignment_info)
    completed_tasks = CompletedAssignmentTask.objects.filter(
        profile=assignment_info.assignment_profile,
        assignment_task__in=completed_tasks_instance
    )
    completed_task_dates = completed_tasks.values_list('created', flat=True)
    dates = {(date.year, date.month, date.day) for date in completed_task_dates}
    filtered_tasks = {
        key: AssignmentTask.objects.filter(
            id__in=completed_tasks.filter(
                       created__year=key[0],
                       created__month=key[1],
                       created__day=key[2]
                   ).order_by('created').values_list('assignment_task', flat=True)
        ) for key in dates
    }
    return render(request, 'assignments/completed_tasks.html', {
        'assignment_info': {
            'uuid': assignment.uuid,
            'info': assignment_info.assignment_info.decode('utf-8')
        },
        'filtered_tasks': reversed(sorted(filtered_tasks.items())),
        'section': 'completed_tasks'
    })


def complete_assigned_task(request, uuid, info, pk):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    task = get_object_or_404(Utils.get_active_tasks_instance(assignment_info), pk=pk)
    with AssignmentTaskActions(assignment, assignment_info) as action:
        action.complete_task(task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cancel_assigned_task(request, uuid, info, pk):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    task = get_object_or_404(Utils.get_completed_tasks_instance(assignment_info), pk=pk)
    with AssignmentTaskActions(assignment, assignment_info) as action:
        action.cancel_task(task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def archive_assigned_task(request, uuid, info, pk):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    task = get_object_or_404(Utils._get_all_tasks_instance(assignment_info), pk=pk)
    with AssignmentTaskActions(assignment, assignment_info) as action:
        action.archive_task(task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_assignment_profile(request, uuid, info):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    if assignment_info.assignment_profile.email == assignment_info.email:
        assignment_info.assignment_profile.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_assignment_list(request, uuid, info):
    assignment, assignment_info = Utils.get_assignment_instances(uuid, parse.unquote(info))
    if assignment_info.assignment_profile.email == assignment_info.email:
        try:
            assignment_profile = assignment_info.assignment_profile
            assignment_profile.assignment_list = assignment.assignment_lists.get(next_list=None)
            assignment_profile.save()
        except ObjectDoesNotExist:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))