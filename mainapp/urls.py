from django.urls import path

from mainapp.views import main, personalcolor_view, style_view, hairloss_view

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('personalcolor_view/', personalcolor_view, name='personalcolor_view'),
    path('style_view/', style_view, name='style_view'),
    path('hairloss_view/', hairloss_view, name='hairloss_view'),
]
