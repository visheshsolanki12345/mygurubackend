from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.pagination import PageNumberPagination

# Create your views here.

##========================== Token Pair =====================================##
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
##========================== End... =================================##


##============================ Register & Token Function =============================##
@api_view(['POST'])
def registerUser(request):
    data = request.data
    # try:
    user = User.objects.create(
        first_name=data['campus'],
        last_name=data['name'],
        username=data['email'],
        email=data['email'],
        password=make_password(data['password'])
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)
    # except:
    #     message = {'detail': 'User with this email already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
##========================== End... =================================##


##============================ Profile Update Function =============================##
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)
##========================== End... =================================##
