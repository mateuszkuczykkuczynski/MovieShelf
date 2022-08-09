import os

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
import requests

OMDB_API_KEY = os.environ.get('OMDB_API_KEY')


def startpage(request):
    return render(request, 'startpage.html')


def homepage(request):
    return render(request, 'homepage.html')


def index(request):
    query = request.GET.get('q')

    if query:
        url = (f"http://www.omdbapi.com/?i=tt3896198&apikey={OMDB_API_KEY}&s=" + query)
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
        }
        template = loader.get_template('search_results.html')

        return HttpResponse(template.render(context, request))

    return render(request, 'index.html')


def pagination(request, query, page_number):
    url = (f"http://www.omdbapi.com/?i=tt3896198&apikey={OMDB_API_KEY}&s=" + query + '&page=' + str(page_number))
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }
    template = loader.get_template('search_results.html')

    return HttpResponse(template.render(context, request))
