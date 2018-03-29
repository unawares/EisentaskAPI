from django.urls import re_path, path, include
from .web_views import active_tasks_view
from .web_views import completed_tasks_view
from .web_views import complete_assigned_task
from .web_views import cancel_assigned_task
from .web_views import archive_assigned_task

app_name = 'protected_assignments_web'
urlpatterns = [
    re_path(r'(?P<uuid>[0-9a-f]{32})/(?P<info>[^/]+)/', include([
        path(r'active-tasks/', active_tasks_view, name='active_tasks'),
        path(r'completed-tasks/', completed_tasks_view, name='completed_tasks'),
        path(r'<int:pk>/', include([
            path(r'complete/', complete_assigned_task, name='complete_assigned_task'),
            path(r'cancel/', cancel_assigned_task, name='cancel_assigned_task'),
            path(r'archive/', archive_assigned_task, name='archive_assigned_task'),
        ])),
    ])),
]
