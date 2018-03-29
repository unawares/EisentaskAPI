from django.urls import re_path, path, include
from .api_views import assign_to
from .api_views import remove_assignment

app_name = 'protected_assignments_api'
urlpatterns = [
    path('assign_to/', assign_to),
    path('remove_assignment/', remove_assignment)
]
