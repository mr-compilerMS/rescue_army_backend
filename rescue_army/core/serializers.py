from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers


class UserSerializer(BaseUserSerializer):
    # avatar = serializers.SerializerMethodField(read_only=True)
    avatar_thumbnail = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def get_avatar_thumbnail(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar_thumbnail.url)
        else:
            return None

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        else:
            return None

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar_thumbnail",
            "avatar",
            "is_staff",
        ]


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "avatar",
        ]
