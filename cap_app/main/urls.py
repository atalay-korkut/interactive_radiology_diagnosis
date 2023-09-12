from django.http import HttpResponse
from django.urls import path
from . import views


urlpatterns = [
    path('', views.image_upload_view),
    path('index/', views.index),
    path('upload/', views.image_upload_view),
    path('generate/', views.generate, name='generate'),
    path('load_model/', views.load_model, name='load_model'),
    path('stats/', views.stats, name='stats'),
    path('comment/', views.comment, name='comment'),
]
