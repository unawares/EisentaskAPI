from rest_framework import serializers


class AssignToSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uuid = serializers.UUIDField(format='hex')
