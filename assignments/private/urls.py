from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AssignmentViewSet

router = SimpleRouter()
router.register(r'', AssignmentViewSet, base_name='assignments')

app_name = 'private_assignments'
urlpatterns = [
    path(r'', include(router.urls)),
]
