from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include("authentication.urls")),
    path('api/carrer/', include("CareerManagementSystem.urls")),
    path('api/video/', include("videoCarrer.urls")),
    path('api/', include("MultipalTestAdd.urls")),
    path('api/comman-function/', include("CommanFunctions.urls")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin

admin.site.site_header = 'My Guru'                    # default: "Django Administration"
admin.site.index_title = "My Guru's Features"                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"