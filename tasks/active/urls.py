from django.urls import path, include

from .views import active_tasks_view


app_name = 'active'
urlpatterns = [
    path(r'', active_tasks_view),
]
