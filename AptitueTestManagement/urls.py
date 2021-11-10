from django.urls import path, include
from AptitueTestManagement import views

##=============================== URL ===============================##
urlpatterns = [
    path('studentquestion', views.getStudent, name="studentquestion"),
]
##=============================== END ===============================##

