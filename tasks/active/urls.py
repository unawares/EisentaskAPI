from django.urls import path, include

from .views import ActiveTasksView, ActiveTasksDetailView


app_name = 'active'
urlpatterns = [
    path(r'', ActiveTasksView.as_view()),
    path(r'<int:pk>/', ActiveTasksDetailView.as_view()),
]
