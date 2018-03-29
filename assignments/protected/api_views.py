from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.http import Http404
from django.db.models import Q
from operator import and_, or_
from functools import reduce
import _pickle as pickle
from uuid import uuid4
from cryptography.fernet import Fernet
from urllib import parse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assignments.models import Assignment
from assignments.models import AssignmentProfile
from assignments.serializers import AssignmentSerializer
from .models import AssignmentInfo
from .serializers import AssignToSerializer
from .serializers import RemoveAssignmentSerializer

def get_assignment_message(email, assignment, assignment_info):
    return (
        assignment.name,
        'http://localhost:8000/web/assignments/%s/%s/active-tasks/' % (assignment.uuid, parse.quote(assignment_info.assignment_info.decode('utf-8'))),
        'from@example.com',
        [email],
    )


def new_assignment_info(assignment, assignment_profile, email, access):
    info = {
        'uuid': uuid4().hex
    }
    b_info = pickle.dumps(info)
    f = Fernet(assignment.key)
    b_assignment_info = f.encrypt(b_info)
    assignment_info = AssignmentInfo()
    assignment_info.assignment_profile = assignment_profile
    assignment_info.assignment_uuid = info['uuid']
    assignment_info.assignment_info = b_assignment_info
    assignment_info.email = email
    assignment_info.access = access
    return assignment_info


@api_view(['POST'])
def assign_to(request):
    ACCESS_EDIT = ACCESS_PRIVATE = 1
    ACCESS_VIEW = ACCESS_PROTECTED = 2
    serializer = AssignToSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    assignment = get_object_or_404(Assignment, uuid=serializer.data['uuid'])
    if (assignment.access == ACCESS_PRIVATE  or assignment.access == ACCESS_PROTECTED):
        if not request.user.is_authenticated or not assignment.creator == request.user:
            raise Http404
    assignment_list = get_object_or_404(assignment.assignment_lists, next_list=None)
    assignment_profile, created = AssignmentProfile.objects.filter(
        assignment_list__in=assignment.assignment_lists.values_list('id')
    ).get_or_create(
        email=serializer.data['email'],
        defaults={
            'assignment_list': assignment_list
        }
    )
    if assignment_profile.assignment_list != assignment_list:
        assignment_profile.assignment_list = assignment_list
        assignment_profile.save()
    objects = {}
    if 'additional' in serializer.data:
        if 'edit_emails' in serializer.data['additional']:
            for email in serializer.data['additional']['edit_emails']:
                objects[email] = new_assignment_info(
                    assignment,
                    assignment_profile,
                    email,
                    ACCESS_EDIT
                )
        if 'view_emails' in serializer.data['additional']:
            for email in serializer.data['additional']['view_emails']:
                objects[email] = new_assignment_info(
                    assignment,
                    assignment_profile,
                    email,
                    ACCESS_VIEW
                )
    objects[serializer.data['email']] = new_assignment_info(
        assignment,
        assignment_profile,
        serializer.data['email'],
        ACCESS_EDIT
    )
    AssignmentInfo.objects \
        .filter(assignment_profile=assignment_profile).delete()
    AssignmentInfo.objects.bulk_create(list(objects.values()))
    messages = (get_assignment_message(email, assignment, objects[email]) for email in objects)
    if assignment.access == ACCESS_PRIVATE:
        assignment.access = ACCESS_PROTECTED
        assignment.save()
    send_mass_mail(messages, fail_silently=False)
    return Response(serializer.data)


@api_view(['POST'])
def remove_assignment(request):
    serializer = RemoveAssignmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    assignment = get_object_or_404(Assignment, uuid=serializer.data['uuid'])
    if not request.user.is_authenticated or not assignment.creator == request.user:
        raise Http404
    assignment_profiles = AssignmentProfile.objects.filter(
        assignment_list__in=assignment.assignment_lists.values_list('id'),
        email=serializer.data['email']
    ).delete()
    return Response(serializer.data)
