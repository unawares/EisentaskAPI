from django.urls import path, include

from .views import ActiveTasksView


app_name = 'active'
urlpatterns = [
    path(r'', ActiveTasksView.as_view()),
]
