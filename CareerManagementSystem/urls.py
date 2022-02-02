from django.urls import path, include
from CareerManagementSystem import views
from rest_framework.routers import DefaultRouter
from CareerManagementSystem import AdminView
router = DefaultRouter()

router.register('counsellor', AdminView.CounsellorAdminViewSet, basename="counsellor")
router.register('student-article', AdminView.StudentArticleAdminViewSet, basename="student-article")
router.register('approve-article', AdminView.EditorAdminViewSet, basename="approve-article")


urlpatterns = [
    path('carrer/', include(router.urls)),
    path('get-carrer-page/', views.getCarrerPage, name="get-carrer-page"),

    # Admin URL
    path('get-carrer-list/', AdminView.get_get_carrer_adminView, name="get-carrer-list"),

]

