from django.urls import path, include

app_name = 'assignments'
urlpatterns = [
    path(r'private/', include('assignments.private.urls', namespace='private')),
    path(r'protected/', include('assignments.protected.api_urls', namespace='protected')),
]
