from django.urls import path, include
from Test_8th import views

##=============================== URL ===============================##
urlpatterns = [
    path('studentquestion', views.getStudent, name="studentquestion"),
    path('question', views.getQuestion, name="question"),
    path('testresult', views.testResult, name="question"),
    path('result', views.getResult, name="result"),
    path('deleteresult', views.delReuslt, name="deleteresult"),
    path('showgrade/', views.showGrade, name="showgrade"),
    path('showindusty/', views.showIndustry, name="showindusty"),
    path('findans/', views.findRightAns, name="findans"),
    path('title/', views.getTitle, name="title"),
]
##=============================== END ===============================##

