from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class GroupTasksRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/(?P<type>active)/priority/(?P<priority>[1234])/groups/(?P<group_id>\d+)/$',
            mapping={'get': 'list_by_priority'},
            name='{basename}-list-active-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/groups/(?P<group_id>\d+)/$',
            mapping={'get': 'list_completed_tasks'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/active/groups/(?P<group_id>\d+)/tasks/$',
            mapping={'post': 'create_group_task'},
            name='{basename}-list-active-tasks',
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/active/groups/(?P<group_id>\d+)/tasks/{lookup}/$',
            mapping={
                'get': 'retrieve_active_group_task',
                'put': 'update_active_group_task',
                'delete': 'delete_active_group_task',
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/completed/groups/(?P<group_id>\d+)/tasks/{lookup}/$',
            mapping={
                'get': 'retrieve_completed_group_task',
                'delete': 'delete_completed_group_task',
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/groups/(?P<group_id>\d+)/dates/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/groups/(?P<group_id>\d+)/dates/(?P<year>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/groups/(?P<group_id>\d+)/dates/(?P<year>\d+)/(?P<month>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/(?P<type>completed)/groups/(?P<group_id>\d+)/dates/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
            mapping={'get': 'list_completed_task_dates'},
            name='{basename}-list-completed-tasks',
            initkwargs={'suffix': 'List'}
        ),
    ]
