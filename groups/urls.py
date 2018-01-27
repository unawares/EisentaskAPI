from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from .views import MyMemberCardViewSet
from .views import MyGroupViewSet
from .views import GroupViewSet
from .views import GroupMemberCardViewSet

router_my = SimpleRouter()
router_my.register(r'member-cards', MyMemberCardViewSet)
router_my.register(r'list', MyGroupViewSet)

router = routers.SimpleRouter()
router.register(r'list', GroupViewSet)

groups_router = routers.NestedSimpleRouter(router, r'list', lookup='group')
groups_router.register(r'member-cards', GroupMemberCardViewSet)

app_name = 'groups'
urlpatterns = [
    path(r'my/', include(router_my.urls)),
    path(r'', include(router.urls)),
    path(r'', include(groups_router.urls)),
]
