
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import Industry
from .serializer import IndustrySerializer
# Create your views here.

@api_view(['GET'])
def getQuestion(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    que = Industry.objects.all()
    result_page = paginator.paginate_queryset(que, request)
    serializer = IndustrySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

