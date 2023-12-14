from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import upload_personal_image, upload_faceshape_image, upload_scalp_image

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('mainapp.urls')),  # mainapp의 urls.py를 포함
    # upload_personal_image 뷰에 대한 경로 추가
    path('upload_personal_image/', upload_personal_image, name='upload_personal_image'),
    # upload_faceshape_image 뷰에 대한 경로 추가
    path('upload_faceshape_image/', upload_faceshape_image, name='upload_faceshape_image'),
    # upload_scalp_image 뷰에 대한 경로 추가
    path('upload_scalp_image/', upload_scalp_image, name='upload_scalp_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
