from rest_framework import serializers


class AdditionalAssignToSerializer(serializers.Serializer):
    edit_emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )
    view_emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )


class AssignToSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uuid = serializers.UUIDField(format='hex')
    additional = AdditionalAssignToSerializer(required=False)


class RemoveAssignmentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uuid = serializers.UUIDField(format='hex')
