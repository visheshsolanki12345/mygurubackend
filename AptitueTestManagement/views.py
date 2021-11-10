from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import TestScheduleManagement, QuestionManagement
from .serializer import TestScheduleManagementSerializer, QuestionManagementSerializer

# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getStudent(request):
    count = QuestionManagement.objects.filter().count()
    que = TestScheduleManagement.objects.all()
    serializer = TestScheduleManagementSerializer(que, many=True)
    context = {'count':count, 'data':serializer.data}
    return Response(context)


@api_view(['GET'])
def getQuestion(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    que = QuestionManagement.objects.all()
    result_page = paginator.paginate_queryset(que, request)
    serializer = QuestionManagementSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
