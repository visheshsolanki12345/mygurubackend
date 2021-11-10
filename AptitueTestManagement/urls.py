from django.urls import path, include
from AptitueTestManagement import views

##=============================== URL ===============================##
urlpatterns = [
    path('studentquestion', views.getStudent, name="studentquestion"),
    path('question', views.getQuestion, name="question"),
]
##=============================== END ===============================##

