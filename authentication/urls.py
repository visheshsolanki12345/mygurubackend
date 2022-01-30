from django.urls import path, include
from authentication import views

##=============================== URL ===============================##
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


##=============================== URL ===============================##
urlpatterns = [
    path('account/login/', views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('account/register/', views.registerUser, name='register'),
    path('account/profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('account/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('account/profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('account/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('account/refresh/', TokenRefreshView.as_view(),name='refresh'),
    path('account/finduser/', views.findUser, name='finduser'),
    path('account/getuser/', views.userPofile, name='getuser'),
    path('account/profile/', views.profileGet, name='profile'),
    path('account/passwordupdate/', views.ChangePasswordView.as_view(), name='passwordupdate'),
]
##=============================== END ===============================##

