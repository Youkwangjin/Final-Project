from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import upload_image  # upload_image 뷰를 import

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('mainapp.urls')),  # mainapp의 urls.py를 포함
    path('upload_image/', upload_image, name='upload_image'),  # upload_image 뷰에 대한 경로 추가
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
