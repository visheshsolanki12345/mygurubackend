from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.pagination import PageNumberPagination
from .models import CareerCategory, Course
from .serializer import CareerCategorySerializer, CourseSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@api_view(['GET'])
def getCarrer(request):
    que = CareerCategory.objects.all()
    serializer = CareerCategorySerializer(que, many=True)
    context = {'data':serializer.data, 'status':status.HTTP_200_OK}
    return Response(context)


# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@api_view(['GET'])
def getCourse(request):
    que = Course.objects.all()
    serializer = CourseSerializer(que, many=True)
    context = {'data':serializer.data, 'status':status.HTTP_200_OK}
    return Response(context)


class CourseViewSet(viewsets.ViewSet):
    # authentication_classes=[JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    ##=========== List =============##
    def list(self, request):
        que = Course.objects.all()
        serializer = CourseSerializer(que, many=True)
        context = {'data':serializer.data, 'status':status.HTTP_200_OK}
        return Response(context)
    ##=========== End... =============##

    ##=========== Retrieve =============##
    def retrieve(self, request, pk=None):
        try:
            queryset = Course.objects.all()
            course = get_object_or_404(queryset, pk=pk)
            serializer = CourseSerializer(course)
            context = {'data':serializer.data, 'status':status.HTTP_202_ACCEPTED}
            return Response(context)
        except:
            context={'message':"Data Not Found", 'status':status.HTTP_400_BAD_REQUEST}
            return Response(context)
    ##=========== End... =============##
##============================== End... =================================##