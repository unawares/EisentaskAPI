from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from assignments.models import Assignment
from assignments.models import AssignmentList
from assignments.protected.web_views import Utils

def public_list_tasks_view(request, uuid):
    ACCESS_PUBLIC = 3
    assignment = get_object_or_404(Assignment, uuid=uuid)
    if assignment.access != ACCESS_PUBLIC:
        raise Http404
    assignment_last_list = get_object_or_404(
        AssignmentList,
        assignment=assignment,
        next_list=None
    )
    tasks = assignment_last_list.assignment_tasks
    orders = assignment_last_list.orders
    f = lambda task: orders[str(task.pk)]
    goals = sorted(tasks.filter(priority=1), key=f)
    progress = sorted(tasks.filter(priority=2), key=f)
    activities = sorted(tasks.filter(priority=3), key=f)
    interruptions = sorted(tasks.filter(priority=4), key=f)
    label_color_class = None
    if assignment.label_color == 1:
        label_color_class = 'goals'
    elif assignment.label_color == 2:
        label_color_class = 'progress'
    elif assignment.label_color == 3:
        label_color_class = 'activities'
    else:
        label_color_class = 'interruptions'
    return render(request, 'assignments_public/public_tasks.html', {
        'uuid': assignment.uuid,
        'name': assignment.name,
        'description': assignment.description,
        'label_color_class': label_color_class,
        'tasks': {
            'goals': goals,
            'progress': progress,
            'activities': activities,
            'interruptions': interruptions
        },
    })
