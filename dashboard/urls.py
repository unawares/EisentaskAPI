from django.urls import path, include
from .views import dashboard

app_name = 'dashboard'
urlpatterns = [
    path(r'', dashboard, name='main')
]
