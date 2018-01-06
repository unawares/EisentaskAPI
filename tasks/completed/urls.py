from django.urls import path, include
from .views import CompletedTasksView, CompletedTasksDetailView

app_name = 'completed'
urlpatterns = [
    path(r'', CompletedTasksView.as_view()),
    path(r'<int:pk>/', CompletedTasksDetailView.as_view()),
]
