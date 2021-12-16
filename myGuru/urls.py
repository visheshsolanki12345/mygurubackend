from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include("StudentManagement.urls")),
    path('api/', include("AptitueTestManagement.urls")),
    path('api/', include("CareerManagementSystem.urls")),
    path('api/6th/', include("Test_6To9.urls")),
    path('api/10th/', include("Test_10.urls")),
    path('api/7th/', include("Test_7th.urls")),
    path('api/8th/', include("Test_8th.urls")),
    path('api/9th/', include("Test_9th.urls")),
    path('api/10th/int/', include("Test_10th_interest.urls")),
    path('api/12th/', include("Test_12th.urls")),
    path('api/videos/', include("videoCarrer.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)