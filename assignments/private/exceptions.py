from rest_framework.exceptions import APIException

class AssignmentActionsError(APIException):
    status_code = 400
    default_detail = 'AssignmentActionsError'
    default_code = 'action_denied'
