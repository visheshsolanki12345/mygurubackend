from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserSerializerWithToken, ChangePasswordSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import UserProfile
from collections import OrderedDict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework_simplejwt.backends import TokenBackend

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.pagination import PageNumberPagination
from threading import Thread
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

class RegisterUserAuth:
    def __init__(self, first_name, last_name, username, email, password):
        Thread.__init__(self)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.getSeriData = ''

    def registerUserFunc(self):
        try:
            userFind = User.objects.get(username = self.username)
            if userFind:
                serializer = UserSerializerWithToken(userFind, many=False)
                self.getSeriData = serializer.data
                return 
        except:
            user = User.objects.create(
                first_name=self.first_name,
                last_name=self.last_name,
                username=self.username,
                email=self.email,
                password=make_password(self.password)
            )
            
            serializer = UserSerializerWithToken(user, many=False)
            self.getSeriData = serializer.data
            return 

##========================== End... =================================##

@api_view(['POST'])
def registerUser(request):
    data = request.data
    first_name=data['campus']
    last_name=data['name']
    username=data['email']
    email=data['email']
    password=data['password']
    reC = RegisterUserAuth(first_name, last_name, username, email, password)
    ru = Thread(target=reC.registerUserFunc)
    ru.start()
    ru.join()
    return Response(reC.getSeriData)



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

##============================ Profile Update Function =============================##
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    data = request.data
    user = request.user
    file = request.FILES
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    serializer = UserSerializerWithToken(user, many=False)
    obj = serializer.data
    try:
        userPic = f"UserProfile/{file['selectedImage']}"
        findId = obj['userData']
        getId = findId['id']
        profileData = UserProfile.objects.filter(id=getId).update(userImage = userPic)
        profileData.save()
    except:
        pass
    # profileData.save()
    # if data['password'] != '':
    #     user.password = make_password(data['password'])
    user.save()
    return Response(OrderedDict(serializer.data))
##========================== End... =================================##


@api_view(['POST'])
def findUser(request):
    # from http.cookies import SimpleCookie
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQwMDc0NTU2LCJqdGkiOiI4ZWQ0OGFkYjE5ZjQ0NGEzYjcyNTNjYmQ3N2EzNzljOCIsInVzZXJfaWQiOjd9.ultv1E4FAt5ybWVyN1541wsr8Z7f4CCrchGyXhiEAds'
    try:
        data = request.data
        token = data['token']
        # print('token', token)
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        userId = valid_data['user_id']
        userData = User.objects.filter(id=userId)
        serializer = UserSerializerWithToken(userData, many=True)
        context = {"data":serializer.data, "status":status.HTTP_202_ACCEPTED}
        return Response(context)
    except:
        context = {'error':'This is not valid user', 'status':status.HTTP_401_UNAUTHORIZED}
        return Response(context)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def profileGet(request):
    user = request.user
    serializer = UserSerializerWithToken(user)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def userPofile(request):
    user = request.user
    getData = UserProfile.objects.filter(user=user)
    serializer = UserProfileSerializer(getData,many=False)
    return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)