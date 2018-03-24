from django.urls import re_path, path, include
from .api_views import assign_to

app_name = 'protected_assignments_api'
urlpatterns = [
    path('assign_to/', assign_to),
]
