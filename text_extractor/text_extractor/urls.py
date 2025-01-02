from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from extractor.views import download_file


urlpatterns = [
    path("admin/", admin.site.urls),
    path("extractor/", include("extractor.urls")),
    path('media/output/<str:file_name>/', download_file, name='download_file'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
