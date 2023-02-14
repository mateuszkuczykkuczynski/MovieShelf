# from django.http import HttpResponse
# from django.template import loader
# from django.utils.text import slugify
# from django.core.paginator import Paginator
import requests
from django.shortcuts import render, get_object_or_404
from environs import Env

from .models import Movie, Actor, Genre, Rating, Director, Writer

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


def movie_details_view(request, imbd_id):
    result = Movie.objects.filter(imbdID=imbd_id).first()

    if not result:
        url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imbd_id}"
        response = request.get(url)
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
            g, created = Genre.objects.get_or_create(name=genre)
            genre_obj.append(g)

        for rating in api_data["Ratings"]:
            r, created = Rating.objects.get_or_create(source=rating["Source"], value=rating["Value"])
            rating_obj.append(r)

        if api_data["Type"] == "movie":
            result = Movie.objects.create(
                Title=api_data["Title"],
                Year=api_data["Year"],
                Rated=api_data["Rated"],
                Released=api_data["Released"],
                Runtime=api_data["Runtime"],
                Plot=api_data["Plot"],
                Language=api_data["Language"],
                Country=api_data["Country"],
                Awards=api_data["Awards"],
                Poster=api_data["Poster"],
                Poster_url=api_data["Poster_url"],
                Metascore=api_data["Metascore"],
                imbdRating=api_data["imbdRating"],
                imbdVotes=api_data["imbdVotes"],
                imbdID=api_data["imbdID"],
                Type=api_data["Type"],
                DVD=api_data["DVD"],
                BoxOffice=api_data["BoxOffice"],
                Production=api_data["Production"],
                Website=api_data["Website"],
            )
            result.Actors.set(actor_obj)
            result.Director.set(director_obj)
            result.Writer.set(writer_obj)
            result.Genre.set(genre_obj)
            result.Rating.set(rating_obj)

        else:
            result = Movie.objects.create(
                Title=api_data["Title"],
                Year=api_data["Year"],
                Rated=api_data["Rated"],
                Released=api_data["Released"],
                Runtime=api_data["Runtime"],
                Plot=api_data["Plot"],
                Language=api_data["Language"],
                Country=api_data["Country"],
                Awards=api_data["Awards"],
                Poster=api_data["Poster"],
                Poster_url=api_data["Poster_url"],
                Metascore=api_data["Metascore"],
                imbdRating=api_data["imbdRating"],
                imbdVotes=api_data["imbdVotes"],
                imbdID=api_data["imbdID"],
                Type=api_data["Type"],
                DVD=api_data["DVD"],
                BoxOffice=api_data["BoxOffice"],
                Production=api_data["Production"],
                Website=api_data["Website"],
                totalSeasons=api_data["totalSeasons"],
            )
            result.Actors.set(actor_obj)
            result.Director.set(director_obj)
            result.Writer.set(writer_obj)
            result.Genre.set(genre_obj)
            result.Rating.set(rating_obj)

    return render(request, 'movie_details.html', {'movie': result})


def actor_details_view(request, name):
    actor = get_object_or_404(Actor, name)
    return render(request, 'actor_details.html', {'actor': actor})


def director_details_view(request, name):
    director = get_object_or_404(Director, name)
    return render(request, 'director_details.html', {'director': director})


def writer_details_view(request, name):
    writer = get_object_or_404(Writer, name)
    return render(request, 'writer_details.html', {'writer': writer})


def genre_detail_view(request, type):
    genre = get_object_or_404(Genre, type)
    return render(request, 'genre_details.html', {'genre': genre})


#
# def pagination(request, query, page_number):
#     url = (f"http://www.omdbapi.com/?i=tt3896198&apikey={OMDB_API_KEY}&s=" + query + '&page=' + str(page_number))
#     response = requests.get(url)
#     movie_data = response.json()
#     page_number = int(page_number) + 1
#
#     context = {
#         'query': query,
#         'movie_data': movie_data,
#         'page_number': page_number,
#     }
#     template = loader.get_template('search_results.html')
#
#     return HttpResponse(template.render(context, request))
#
#
# def movieDetails(request, imdb_id):
#     if Movie.objects.filter(imdbID=imdb_id).exists():
#         movie_data = Movie.objects.get(imdbID=imdb_id)
#         site_database = True
#
#         context = {
#             'movie_data': movie_data,
#             'site_database': site_database,
#         }
#
#     else:
#         url = (f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i=" + imdb_id)
#         response = requests.get(url)
#         movie_data = response.json()
#
#         actor_objects = []
#         genre_objects = []
#         rating_objects = []
#
#         actor_list = [x.strip() for x in movie_data['Actors'].split(',')]
#
#         for actor in actor_list:
#             a, created = Actor.objects.get_or_create(name=actor)
#             actor_objects.append(a)
#
#         genre_list = list(movie_data['Genre'].replace(" ", "").split(','))
#
#         for genre in genre_list:
#             genre_slug = slugify(genre)
#             g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
#             genre_objects.append(g)
#
#         for rate in movie_data['Ratings']:
#             r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
#             rating_objects.append(r)
#
#         if movie_data['Type'] == 'movie':
#             m, created = Movie.objects.get_or_create(
#                 Title=movie_data['Title'],
#                 Year=movie_data['Year'],
#                 Rated=movie_data['Rated'],
#                 Released=movie_data['Released'],
#                 Runtime=movie_data['Runtime'],
#                 Director=movie_data['Director'],
#                 Writer=movie_data['Writer'],
#                 Plot=movie_data['Plot'],
#                 Language=movie_data['Language'],
#                 Country=movie_data['Country'],
#                 Awards=movie_data['Awards'],
#                 Poster_url=movie_data['Poster'],
#                 Metascore=movie_data['Metascore'],
#                 imdbRating=movie_data['imdbRating'],
#                 imdbVotes=movie_data['imdbVotes'],
#                 imdbID=movie_data['imdbID'],
#                 Type=movie_data['Type'],
#                 DVD=movie_data['DVD'],
#                 BoxOffice=movie_data['BoxOffice'],
#                 Production=movie_data['Production'],
#                 Website=movie_data['Website'],
#             )
#
#             m.Genre.set(genre_objects)
#             m.Actors.set(actor_objects)
#             m.Ratings.set(rating_objects)
#
#         else:
#             m, created = Movie.objects.get_or_create(
#                 Title=movie_data['Title'],
#                 Year=movie_data['Year'],
#                 Rated=movie_data['Rated'],
#                 Released=movie_data['Released'],
#                 Runtime=movie_data['Runtime'],
#                 Director=movie_data['Director'],
#                 Writer=movie_data['Writer'],
#                 Plot=movie_data['Plot'],
#                 Language=movie_data['Language'],
#                 Country=movie_data['Country'],
#                 Awards=movie_data['Awards'],
#                 Poster_url=movie_data['Poster'],
#                 Metascore=movie_data['Metascore'],
#                 imdbRating=movie_data['imdbRating'],
#                 imdbVotes=movie_data['imdbVotes'],
#                 imdbID=movie_data['imdbID'],
#                 Type=movie_data['Type'],
#                 totalSeasons=movie_data['totalSeasons']
#             )
#
#             m.Genre.set(genre_objects)
#             m.Actors.set(actor_objects)
#             m.Ratings.set(rating_objects)
#
#         for actor in actor_objects:
#             actor.movies.add(m)
#             actor.save()
#
#         m.save()
#         site_database = False
#
#         context = {
#             'movie_data': movie_data,
#             'site_database': site_database
#
#         }
#
#         template = loader.get_template('movie_details.html')
#
#         return HttpResponse(template.render(context, request))
#
#
# def genres(request, genre_slug):
#     genre = get_object_or_404(Genre, slug=genre_slug)
#     movies = Movie.objects.filter(Genre=genre)
#
#     paginator = Paginator(movies, 9)
#     page_number = request.GET.get('page')
#     movie_data = paginator.get_page(page_number)
#
#     context = {
#         'movie_data': movie_data,
#         'genre': genre
#     }
#
#     template = loader.get_template('genre.html')
#
#     return HttpResponse(template.render(context, request))
#
#
# def actors(request, actor_slug):
#     actor = get_object_or_404(Actor, slug=actor_slug)
#     movies = Movie.objects.filter(Actors=actor)
#
#     paginator = Paginator(movies, 9)
#     page_number = request.GET.get('page')
#     movie_data = paginator.get_page(page_number)
#
#     context = {
#         'movie_data': movie_data,
#         'actor': actor
#     }
#
#     template = loader.get_template('actors.html')
#
#     return HttpResponse(template.render(context, request))
