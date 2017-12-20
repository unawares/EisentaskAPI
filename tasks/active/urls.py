from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ActiveTasksViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', ActiveTasksViewSet, base_name='ActiveTasks')

# The API URLs are now determined automatically by the router.
app_name = 'active'
urlpatterns = [
    path(r'', include(router.urls)),
]
