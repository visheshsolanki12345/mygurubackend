from django.urls import path
from videoCarrer import views


##=============================== URL ===============================##
urlpatterns = [
    path('youtube-video/', views.getYouTubVideo, name="youtube-video"),
]
##=============================== END ===============================##

