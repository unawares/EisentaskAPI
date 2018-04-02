from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.
class ProfilesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile, created = Profile.objects.get_or_create(owner=self.request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile, created = Profile.objects.get_or_create(owner=self.request.user)
        if 'data' in serializer.data:
            profile.data = serializer.data['data']
            profile.save()
        return Response(ProfileSerializer(profile).data)
