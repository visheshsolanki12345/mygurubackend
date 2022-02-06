from threading import Thread
from urllib import request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
import time

from CareerManagementSystem.models import Carrer
from CareerManagementSystem.models import EditorApproveArticle
from .models import (
    YouTubeVideo, VideoCarrer, VideoNoView, VideoRating
)

from .serializer import (
    YouTubeVideoSerializer, VideoCarrerSerializer,VideoCarrerSerializer
)
from CareerManagementSystem import views 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


videoCarrerIdContext = {}
videoCarrerSingleDataContext = {}
videoCarrerIncViewContext = {}
videoCarrerRatingContext = {}


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

def get_video_carrer_func(id, request, check):
    if check == "id":
        if id in videoCarrerIdContext:
            return videoCarrerIdContext[id]
    
    if check == "carrerPage":
        if id in views.carrerIdContext:
            id = views.carrerIdContext[id]
        carrerId = Carrer.objects.get(id = id)
        obj = VideoCarrer.objects.filter(carrer = carrerId, rating__gte=4).order_by('-createAt')[:10]
        serializer = VideoCarrerSerializer(obj, many=True)
        return serializer.data
    
    if check == "singleData":
        t = Thread(target=no_view_video, args=(request.user, id))
        t.start()
        t.join()
        if id in videoCarrerSingleDataContext:
            return videoCarrerSingleDataContext[id]
        obj = VideoCarrer.objects.get(id = id)
        serializer = VideoCarrerSerializer(obj, many=False)
        videoCarrerSingleDataContext[id] = serializer.data
        return serializer.data

    if check == "paginationSearch":
        query = request.query_params.get('keyword')
        if query == None:
            query = ''
            # obj = VideoCarrer.objects.filter().order_by('-createAt')[:10]
            obj = VideoCarrer.objects.filter().order_by('-createAt')
        else:
            if query in views.carrerIdContext:
                carrerSearch = views.carrerIdContext[query]
            carrerSearch = Carrer.objects.get(id = query) 
            views.carrerIdContext[query] = carrerSearch
            obj = VideoCarrer.objects.filter(carrer=carrerSearch).order_by('-createAt')
        page = request.query_params.get('page')
        paginator = Paginator(obj,1)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        serializer = VideoCarrerSerializer(obj, many=True)
        context = {'videoCarrer': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context



    # if check == "incView":
    #     incMent = 1
    #     if id in videoCarrerIncViewContext:
    #         incMent = videoCarrerIdContext[id] + 1
    #         videoCarrerIdContext[id] = incMent
    #     obj = VideoCarrer.objects.filter(id = id).update(noView = incMent)
    #     videoCarrerIdContext[id] = obj.noView
    #     return

    if check == "incView":
        obj = VideoCarrer.objects.get(id = id)
        obj.noView += 1
        obj.save()
        return


def no_view_video(user, id):
    obj = VideoCarrer.objects.get(id = id)
    if VideoNoView.objects.filter(videoCarrer = obj, user = user).exists():
        return
    else:
        VideoNoView.objects.create(
            user = user, 
            videoCarrer = obj,
            noView = 1,
        )
        obj.noView = obj.noView + 1
        obj.save()  
        return

    
class videoCarrerClass:
    def __init__(self):
        Thread.__init__(self)
        self.allData = ''
        self.singleData = ''
    
    def get_all_data(self, id, request, check):
        self.allData = get_video_carrer_func(id, request, check)
        return
    
    def get_single_data(self, id, request, check):
        self.singleData = get_video_carrer_func(id, request, check)
        return


class VideoCarrerViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # start = time.time()
        classOj = videoCarrerClass()
        vl = Thread(target=classOj.get_all_data, args=("null", request, "paginationSearch"))
        vl.start()
        vl.join()
        # end = time.time()
        # print(f"Runtime of the program is {end - start}")
        return Response(classOj.allData)
    
    def retrieve(self, request, pk=None):
        classOj = videoCarrerClass()
        sdt = Thread(target=classOj.get_single_data, args=(pk, request, "singleData"))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)


videoSignal = ''

@api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def videoView(request, pk):
    data = request.data
    user = request.user
    global videoSignal
    def rating_count(pk):
        global videoSignal
        obj = VideoCarrer.objects.get(id = pk)
        if VideoRating.objects.filter(user = user, videoCarrer  = obj).exists():
            videoSignal = False
            return 
        else:
            VideoRating.objects.create(
                user = user,
                videoCarrer = obj,
                rating = data['rating'],
            )
            ratingCount = obj.rating
            obj.rating = ((5 * ratingCount) + data['rating']) / (ratingCount + 1)
            obj.save()
            videoSignal = True
            return 
    t = Thread(target=rating_count, args=(pk,))
    t.start()
    t.join()
    if videoSignal == True:
        videoSignal = ''
        return Response(status.HTTP_201_CREATED)
    else:
        videoSignal = ''
        return Response(status.HTTP_208_ALREADY_REPORTED)




