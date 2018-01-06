from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', TaskViewSet, base_name='Task')

# The API URLs are now determined automatically by the router.
app_name = 'tasks'
urlpatterns = [
    path(r'active/', include('tasks.active.urls', namespace='active')),
    path(r'completed/', include('tasks.completed.urls', namespace='completed')),
    path(r'', include(router.urls)),
]
