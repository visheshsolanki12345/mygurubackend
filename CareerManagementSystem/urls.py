from django.urls import path, include
from CareerManagementSystem import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename="courses")
##=============================== URL ===============================##
urlpatterns = [
    path('', include(router.urls)),
    path('carrer', views.getCarrer, name="carrer"),
]
##=============================== END ===============================##

