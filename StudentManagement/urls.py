from django.urls import path, include
from StudentManagement import views

##=============================== URL ===============================##
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


##=============================== URL ===============================##
urlpatterns = [
    path('account/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('account/register/', views.registerUser, name='register'),
    path('account/profile/update/', views.updateUserProfile, name="user-profile-update"),
]
##=============================== END ===============================##

