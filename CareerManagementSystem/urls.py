from django.urls import path, include
from CareerManagementSystem import views
from rest_framework.routers import DefaultRouter
from CareerManagementSystem import AdminView
router = DefaultRouter()

# Admin Url
router.register('counsellor', AdminView.CounsellorAdminViewSet, basename="counsellor")
router.register('approve-article', AdminView.EditorAdminViewSet, basename="approve-article")
router.register('student-article-editorBy', AdminView.StudentArticleEditoryByAdminViewSet, basename="student-article-editorBy")

# User Url
router.register('counsellor-get', views.CounsellorViewSet, basename="counsellor-get")
router.register('get-article', views.EditorViewSet, basename="get-article")
router.register('student-article', AdminView.StudentArticleAdminViewSet, basename="student-article")


urlpatterns = [
    path('', include(router.urls)),
    path('get-carrer-page/<str:id>/', views.getCarrerPage, name="get-carrer-page"),
    path('article-rating/<str:pk>/', views.articleRating, name="article-rating"),
    path('counsellor-rating/<str:pk>/', views.counsellorRating, name="counsellor-rating"),
    path('get-all-article/', views.getAllArticle, name="article-rating"),
    path('slot-booking/<str:pk>/', views.slotBooking, name="slot-booking"),

    # Admin URL
    path('get-carrer-list/', AdminView.get_get_carrer_adminView, name="get-carrer-list"),

]

