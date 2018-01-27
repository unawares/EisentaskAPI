from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Group
from .models import MemberCard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'id',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('created', 'updated',)


class MemberCardSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = MemberCard
        fields = '__all__'


class UsernameOrEmailSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=150, required=True)
