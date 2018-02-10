from rest_framework.exceptions import APIException

class GroupAdminActionsError(APIException):
    status_code = 400
    default_detail = 'GroupAdminActionsError'
    default_code = 'action_denied'

class GroupAdminActionsOnUserError(APIException):
    status_code = 400
    default_detail = 'GroupAdminActionsOnUserError'
    default_code = 'action_denied'

class GroupAdminActionsNoMemberError(APIException):
    status_code = 400
    default_detail = 'GroupAdminActionsNoMemberError'
    default_code = 'action_denied'
