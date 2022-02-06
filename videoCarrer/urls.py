from django.urls import path, include
from videoCarrer import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


router.register('video', views.VideoCarrerViewSet, basename="video")

##=============================== URL ===============================##
urlpatterns = [
    path('', include(router.urls)),
    path('youtube/', views.getYouTubVideo, name="youtube"),


    path('video-views/<str:pk>/', views.videoView, name="video-views"),
]
##=============================== END ===============================##

