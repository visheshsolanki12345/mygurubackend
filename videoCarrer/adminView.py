
from threading import Thread
from urllib import request
from html5lib import serialize
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
import time
from CareerManagementSystem.models import Carrer
from .models import VideoCarrer
from .serializer import VideoCarrerSerializer

class VideoCarrerAdminViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    # authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        obj = VideoCarrer.objects.all()
        serializer = VideoCarrerSerializer(obj, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = VideoCarrer.objects.get(id = pk)
        serializer = VideoCarrerSerializer(obj, many=False)
        return Response(serializer.data)
    
    def create(self, request):
        data = request.data
        file = request.FILES
        user = request.user
        carrerId = data['carrerId']
        carrerObj = Carrer.objects.get(id = carrerId)
        VideoCarrer.objects.create(
            user = user,
            carrer = carrerObj,
            title = data['title'],
            sortDescription = data['sortDescription'],
            thumbnailImage = file['thumbnailImage'],
            embedUrl = data['embedUrl'],
            price = data['price'],
        )
        return Response(status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        file = request.FILES
        VideoCarrer.objects.filter(id = pk).update(
            title = data['title'],
            sortDescription = data['sortDescription'],
            thumbnailImage = file['thumbnailImage'],
            embedUrl = data['embedUrl'],
            price = data['price'],
        )        
        return Response(status.HTTP_202_ACCEPTED)


    def destroy(self, request, pk=None):
        VideoCarrer.objects.filter(id = pk).delete()
        return Response(status.HTTP_200_OK)
