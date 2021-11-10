from django.urls import path, include
from CareerManagement import views

##=============================== URL ===============================##
urlpatterns = [
    path('question', views.getQuestion, name="question"),
    # path('studentquestion', views.getStudent, name="studentquestion"),
]
##=============================== END ===============================##

