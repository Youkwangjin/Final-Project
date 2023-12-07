from django.urls import path

from mainapp.views import main, camera_view

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('camera_view/', camera_view, name='camera_view'),
]