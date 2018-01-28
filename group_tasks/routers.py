from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class GroupTasksRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/(?P<type>(?:active)|(?:completed))/priority/(?P<priority>[1234])/group/(?P<group_id>\d+)/$',
            mapping={'get': 'list_by_priority'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>(?:active)|(?:completed))/group/(?P<group_id>\d+)/task/{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
    ]
