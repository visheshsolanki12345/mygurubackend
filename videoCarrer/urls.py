from django.urls import path, include
from videoCarrer import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from . import adminView

router.register('video', views.VideoCarrerViewSet, basename="video")



# AdminURl
router.register('video-admin', adminView.VideoCarrerAdminViewSet, basename="video-admin")
##=============================== URL ===============================##
urlpatterns = [
    path('', include(router.urls)),
    path('youtube/', views.getYouTubVideo, name="youtube"),
    path('all-video/', views.allVideoFunc, name="all-video"),
    path('parches-videos/', views.parches_video, name="all-video"),


    path('video-views/<str:pk>/', views.videoView, name="video-views"),
]
##=============================== END ===============================##

