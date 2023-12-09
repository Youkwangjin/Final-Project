from django.urls import path

from mainapp.views import main, personalcolor_view, style_view, hairloss_view, hairlossresult_view,personalcolorresult_view,styleresult_view

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('personalcolor_view/', personalcolor_view, name='personalcolor_view'),
    path('style_view/', style_view, name='style_view'),
    path('hairloss_view/', hairloss_view, name='hairloss_view'),
    path('hairlossresult_view/', hairlossresult_view, name='hairlossresult_view'),
    path('personalcolorresult_view/', personalcolorresult_view, name='personalcolorresult_view'),
    path('styleresult_view/', styleresult_view, name='styleresult_view'),
]
