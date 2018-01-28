from django.urls import path, include
from group_tasks.routers import GroupTasksRouter
from .views import GroupTasksViewSet

router_group_tasks = GroupTasksRouter()
router_group_tasks.register(r'', GroupTasksViewSet, base_name='group_tasks')

app_name = 'group_tasks'
urlpatterns = [
    path(r'', include(router_group_tasks.urls)),
]
