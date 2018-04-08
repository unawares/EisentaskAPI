from django.urls import re_path, path, include
from .web_views import public_list_tasks_view

app_name = 'public_assignments_web'
urlpatterns = [
    re_path(r'(?P<uuid>[0-9a-f]{32})/', include([
        path(r'', public_list_tasks_view, name='public_list_tasks_view'),
    ])),
]
