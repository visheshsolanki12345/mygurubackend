from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import YouTubeVideo
from .serializer import YouTubeVideoSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getYouTubVideo(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    que = YouTubeVideo.objects.all()
    result_page = paginator.paginate_queryset(que, request)
    serializer = YouTubeVideoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)