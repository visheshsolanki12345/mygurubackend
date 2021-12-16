from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
##=============================== User Serializer ==================================##
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name','last_name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

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
        fields = ['id', 'username', 'email', 'name','last_name', 'isAdmin', 'token', 'profile']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
##=============================== End... ==================================##


