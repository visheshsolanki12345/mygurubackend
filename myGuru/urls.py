from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include("StudentManagement.urls")),
    path('api/', include("CareerManagement.urls")),
    path('api/', include("AptitueTestManagement.urls")),
]
