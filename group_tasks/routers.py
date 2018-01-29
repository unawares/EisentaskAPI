from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class GroupTasksRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/(?P<type>active)/priority/(?P<priority>[1234])/group/(?P<group_id>\d+)/$',
            mapping={'get': 'list_by_priority'},
            name='{basename}-list-active-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/group/(?P<group_id>\d+)/$',
            mapping={'get': 'list_completed_tasks'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/group/(?P<group_id>\d+)/dates/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/group/(?P<group_id>\d+)/dates/(?P<year>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/group/(?P<group_id>\d+)/dates/(?P<year>\d+)/(?P<month>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/group/(?P<group_id>\d+)/dates/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>(?:active)|(?:completed))/group/(?P<group_id>\d+)/task/{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
    ]
