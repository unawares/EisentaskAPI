from django.urls import path, include
from .views import headpage

app_name = 'headpage'
urlpatterns = [
    path(r'', headpage, name='main'),
]
