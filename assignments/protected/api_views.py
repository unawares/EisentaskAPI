from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import _pickle as pickle
from uuid import uuid4
from cryptography.fernet import Fernet
from urllib import parse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assignments.models import Assignment
from assignments.models import AssignmentProfile
from .models import AssignmentInfo
from .serializers import AssignToSerializer

def send_assignment(email, assignment_info):
    send_mail(
        'Assignment',
        'http://localhost:8000/web/assignments/%s/%s/' % (assignment_info.assignment_profile.assignment_list.assignment.uuid, parse.quote(assignment_info.assignment_info.decode('utf-8'))),
        'from@example.com',
        [email],
        fail_silently=False,
    )


@api_view(['POST'])
def assign_to(request):
    serializer = AssignToSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    assignment = get_object_or_404(Assignment, uuid=serializer.data['uuid'])
    assignment_list = get_object_or_404(assignment.assignment_lists, next_list=None)
    assignment_profile, created = AssignmentProfile.objects.get_or_create(
        email=serializer.data['email'],
        assignment_list=assignment_list
    )
    info = {
        'uuid': uuid4().hex
    }
    b_info = pickle.dumps(info)
    f = Fernet(assignment.key)
    b_assignment_info = f.encrypt(b_info)
    AssignmentInfo.objects.filter(assignment_profile=assignment_profile).delete()
    assignment_info = AssignmentInfo()
    assignment_info.assignment_profile = assignment_profile
    assignment_info.assignment_uuid = info['uuid']
    assignment_info.assignment_info = b_assignment_info
    assignment_info.save()
    send_assignment(assignment_profile.email, assignment_info)
    return Response(serializer.data)
