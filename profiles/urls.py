from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfilesView

app_name = 'profiles'
urlpatterns = [
    path(r'me/', ProfilesView.as_view())
]
