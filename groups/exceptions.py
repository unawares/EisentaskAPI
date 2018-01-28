from rest_framework.exceptions import APIException

class GroupAdminActionsError(APIException):
    status_code = 400
    default_detail = 'User has not admin privileges.'
    default_code = 'access_denied'

class GroupAdminActionsOnUserError(APIException):
    status_code = 400
    default_detail = 'User has admin privileges.'
    default_code = 'access_denied'

class GroupAdminActionsNoMemberError(APIException):
    status_code = 400
    default_detail = 'User must be member of the group.'
    default_code = 'access_denied'
