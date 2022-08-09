from django.urls import path
from . import views

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('homepage', views.homepage, name='homepage'),
    path('index', views.index, name='index')

]
