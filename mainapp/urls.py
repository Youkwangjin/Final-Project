from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mainapp.views import main, personalcolor_view, style_view, hairloss_view, hairlossresult_view
from mainapp.views import personalcolorresult_view

# from mainapp.views import styleresult_view
app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('personalcolor_view/', personalcolor_view, name='personalcolor_view'),
    path('style_view/', style_view, name='style_view'),
    path('hairloss_view/', hairloss_view, name='hairloss_view'),
    path('hairlossresult_view/', hairlossresult_view, name='hairlossresult_view'),
    path('personalcolorresult_view/', personalcolorresult_view, name='personalcolorresult_view'),
    # path('styleresult_view/', styleresult_view, name='styleresult_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
