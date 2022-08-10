from django.urls import path
from . import views
from scenario.views import pagination

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('homepage', views.homepage, name='homepage'),
    path('index', views.index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination')

]
