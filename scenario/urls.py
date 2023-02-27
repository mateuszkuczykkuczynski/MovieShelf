from django.urls import path
from .views import (
    homepage_view,
    movie_details_view,
    actor_details_view,
    director_details_view,
    writer_details_view,
    genre_detail_view,
    PositionsWatchedByUserView,
    PositionsToWatchByUserView
)

urlpatterns = [path('', homepage_view, name='home'),
               path('result/<result_id>', movie_details_view, name='movie_details'),
               path('actor/<slug:actor_slug>', actor_details_view, name='actor_detail'),
               path('director/<slug:director_slug>', director_details_view, name='director_detail'),
               path('writer/<slug:writer_slug>', writer_details_view, name='writer_detail'),
               path('genre/<slug:genre_slug>', genre_detail_view, name='genre_type'),
               path('users/<int:user_id>/watched', PositionsWatchedByUserView.as_view(), name='watched_by_user'),
               path('users/<int:user_id>/to_watch', PositionsToWatchByUserView.as_view(), name='to_watch_by_user')]

# urlpatterns = [
#     path('', views.startpage, name='startpage'),
#     path('homepage', views.homepage, name='homepage'),
#     path('index', views.index, name='index'),
#     path('search/<query>/page/<page_number>', views.pagination, name='pagination'),
#     path('<imdb_id>', views.movieDetails, name='movie_details'),
#     path('genre/<genre_slug>', views.genres, name='genres'),
#     path('actors/<actors_slug>', views.actors, name='actors')
#
# ]
