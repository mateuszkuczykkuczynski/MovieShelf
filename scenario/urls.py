from django.urls import path
from . import views


urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('homepage', views.homepage, name='homepage'),
    path('index', views.index, name='index'),
    path('search/<query>/page/<page_number>', views.pagination, name='pagination'),
    path('<imdb_id>', views.movieDetails, name='movie_details'),
    path('genre/<genre_slug>', views.genres, name='genres'),
    path('actors/<actors_slug>', views.actors, name='actors')

]
