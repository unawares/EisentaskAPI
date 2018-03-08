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
from django.urls import re_path, path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from allauth.account.views import password_reset_from_key

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

api_patterns = [
    path(r'tasks/', include('tasks.urls', namespace='tasks')),
    path(r'group_tasks/', include('group_tasks.urls', namespace='group_tasks')),
    path(r'groups/', include('groups.urls', namespace='groups')),
    path(r'auth/', include('rest_auth.urls')),
    path(r'auth/registration/', include('rest_auth.registration.urls')),
    path(r'token-auth/', obtain_jwt_token),
    path(r'token-refresh/', refresh_jwt_token),
]

web_patterns = [
    path(r'', include('headpage.urls', namespace='headpage')),
    path(r'dashboard/', include('dashboard.urls', namespace='dashboard')),
    re_path(r'accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         password_reset_confirm,
         name='password_reset_confirm'),
    re_path(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
    path(r'accounts/', include('allauth.urls')),
]

urlpatterns = [
    path(r'', RedirectView.as_view(pattern_name='headpage:main', permanent=False)),
    path(r'admin/', admin.site.urls),
    path(r'api/', include(api_patterns)),
    path(r'web/', include(web_patterns)),
]
