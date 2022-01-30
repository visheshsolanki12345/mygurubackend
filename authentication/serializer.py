from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from authentication.models import UserProfile
##=============================== User Serializer ==================================##
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    access = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name','last_name', 'isAdmin', 'access']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_access(self, obj):
        return str(AccessToken.for_user(obj))

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
##=============================== End... ==================================##

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'className','userPic']


##=============================== User Serializer With Token ==================================##
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    profile = UserProfileSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name','last_name', 'isAdmin', 'token', 'access', 'profile']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
##=============================== End... ==================================##


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)