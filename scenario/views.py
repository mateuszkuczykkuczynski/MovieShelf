# from django.http import HttpResponse
# from django.template import loader
# from django.utils.text import slugify
# from django.core.paginator import Paginator

import requests
from django.shortcuts import render, get_object_or_404
from environs import Env
from django.utils.text import slugify
from .models import Movie, Actor, Genre, Rating, Director, Writer, WatchedByUser, ToWatchByUser
from django.views.generic import ListView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


env = Env()
env.read_env()

OMDB_API_KEY = env.str("OMDB_API_KEY")


def homepage_view(request):
    query = request.GET.get('q')
    if query:
        url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
        response = requests.get(url)
        results = response.json()
        return render(request, 'search_results.html', {
            'results': results
        })

    return render(request, 'home.html')


def movie_details_view(request, result_id):

    if Movie.objects.filter(imdbID=result_id).exists():
        api_data = Movie.objects.get(imdbID=result_id)
        our_db = True

        context = {
            'result': api_data,
            'our_db': our_db,
        }

    else:
        url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={result_id}"
        response = requests.get(url)
        api_data = response.json()

        actor_obj = []
        director_obj = []
        writer_obj = []
        genre_obj = []
        rating_obj = []

        actors_list = [x.strip() for x in api_data["Actors"].split(",")]
        for actor in actors_list:
            a, created = Actor.objects.get_or_create(name=actor)
            actor_obj.append(a)

        director_list = [x.strip() for x in api_data["Director"].split(",")]
        for director in director_list:
            d, created = Director.objects.get_or_create(name=director)
            director_obj.append(d)

        writer_list = [x.strip() for x in api_data["Writer"].split(",")]
        for writer in writer_list:
            w, created = Writer.objects.get_or_create(name=writer)
            writer_obj.append(w)

        genre_list = [x.strip() for x in api_data["Genre"].split(",")]
        for genre in genre_list:
            g, created = Genre.objects.get_or_create(genre_type=genre)
            genre_obj.append(g)

        for rating in api_data["Ratings"]:
            r, created = Rating.objects.get_or_create(source=rating["Source"], value=rating["Value"])
            rating_obj.append(r)

        if api_data["Type"] == "movie":
            data, created = Movie.objects.get_or_create(
                Title=api_data["Title"],
                Year=api_data["Year"],
                Rated=api_data["Rated"],
                Released=api_data["Released"],
                Runtime=api_data["Runtime"],
                Plot=api_data["Plot"],
                Language=api_data["Language"],
                Country=api_data["Country"],
                Awards=api_data["Awards"],
                Poster_url=api_data["Poster"],
                Metascore=api_data["Metascore"],
                imdbRating=api_data["imdbRating"],
                imdbVotes=api_data["imdbVotes"],
                imdbID=api_data["imdbID"],
                Type=api_data["Type"],
                DVD=api_data["DVD"],
                BoxOffice=api_data["BoxOffice"],
                Production=api_data["Production"],
                Website=api_data["Website"],
            )
            data.Actors.set(actor_obj)
            data.Director.set(director_obj)
            data.Writer.set(writer_obj)
            data.Genre.set(genre_obj)
            data.Rating.set(rating_obj)

        else:
            data, created = Movie.objects.get_or_create(
                Title=api_data["Title"],
                Year=api_data["Year"],
                Rated=api_data["Rated"],
                Released=api_data["Released"],
                Runtime=api_data["Runtime"],
                Plot=api_data["Plot"],
                Language=api_data["Language"],
                Country=api_data["Country"],
                Awards=api_data["Awards"],
                Poster_url=api_data["Poster"],
                Metascore=api_data["Metascore"],
                imdbRating=api_data["imdbRating"],
                imdbVotes=api_data["imdbVotes"],
                imdbID=api_data["imdbID"],
                Type=api_data["Type"],
                totalSeasons=api_data["totalSeasons"],
            )
            data.Actors.set(actor_obj)
            data.Director.set(director_obj)
            data.Writer.set(writer_obj)
            data.Genre.set(genre_obj)
            data.Rating.set(rating_obj)

        data.save()
        our_db = False

        context = {
            'result': api_data,
            'our_db': our_db,
        }

    return render(request, 'movie_details.html', context)


def actor_details_view(request, actor_slug):
    actor = get_object_or_404(Actor, slug=actor_slug)
    if actor.slug is None:
        actor.slug = slugify(actor.name)
        actor.save()
    actor_movies = actor.movie_actor.values_list("Title", flat=True)
    return render(request, 'actor_details.html', {'actor': actor,
                                                  'actor_movies': actor_movies})


def director_details_view(request, director_slug):
    director = get_object_or_404(Director, slug=director_slug)
    director_movies = director.movie_director.values_list("Title", flat=True)
    return render(request, 'director_details.html', {'director': director,
                                                     'director_movies': director_movies})


def writer_details_view(request, writer_slug):
    writer = get_object_or_404(Writer, slug=writer_slug)
    writer_movies = writer.movie_writer.values_list("Title", flat=True)
    return render(request, 'writer_details.html', {'writer': writer,
                                                   'writer_movies': writer_movies})


def genre_detail_view(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    genre_results = genre.movie_genre.values_list("Title", flat=True)
    return render(request, 'genre_details.html', {'genre': genre,
                                                  'genre_results': genre_results})


class PositionsWatchedByUserView(ListView):
    model = WatchedByUser
    template_name = "watched_by_user.html"
    context_object_name = "watched_all"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), id=user_id)
        return user.watched_position.all()


class PositionsToWatchByUserView(ListView):
    model = ToWatchByUser
    template_name = "to_watch_by_user.html"
    context_object_name = "to_watch_all"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), id=user_id)
        return user.position_to_watch.all()


class PositionAddWatchedView(LoginRequiredMixin, CreateView):
    model = WatchedByUser
    fields = ['movies']
