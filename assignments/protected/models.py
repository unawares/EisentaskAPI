from django.db import models
from django.urls import reverse
import base64
from urllib import parse
from assignments.models import AssignmentProfile

# Create your models here.

class AssignmentInfo(models.Model):
    assignment_profile = models.OneToOneField(
        AssignmentProfile,
        related_name='assignment_infos',
        on_delete=models.CASCADE
    )
    assignment_uuid = models.CharField(max_length=32)
    _assignment_info = models.TextField(db_column='assignment_info')
    def assignment_info():
        def fget(self):
            return base64.decodestring(str.encode(self._assignment_info, 'utf-8'))
        def fset(self, assignment_info):
            self._assignment_info = base64.encodestring(assignment_info).decode('utf-8')
        return locals()
    assignment_info = property(**assignment_info())

    def get_absolute_url(self):
        return reverse(
            'assignments.protected_web:active_tasks',
            kwargs={
                'uuid': self.assignment_profile.assignment_list.assignment.uuid,
                'info': parse.quote(self.assignment_info.decode('utf-8'))
            }
        )
