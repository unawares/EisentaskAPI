"""eisentask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

api_patterns = [
    path(r'tasks/', include('tasks.urls', namespace='tasks')),
    path(r'auth/', include('rest_auth.urls')),
    path(r'auth/registration/', include('rest_auth.registration.urls')),
    path(r'token-auth/', obtain_jwt_token),
    path(r'token-refresh/', refresh_jwt_token),
]

web_patterns = [
    path(r'dashboard/', include('dashboard.urls', namespace='dashboard')),
    path(r'accounts/', include('allauth.urls')),
]

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(api_patterns)),
    path(r'web/', include(web_patterns)),
]
