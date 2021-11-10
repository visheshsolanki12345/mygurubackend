from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import TestScheduleManagement
from .serializer import TestScheduleManagementSerializer
from CareerManagement.models import Industry

# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getStudent(request):
    count = Industry.objects.filter().count()
    que = TestScheduleManagement.objects.all()
    serializer = TestScheduleManagementSerializer(que, many=True)
    context = {'count':count, 'data':serializer.data}
    return Response(context)