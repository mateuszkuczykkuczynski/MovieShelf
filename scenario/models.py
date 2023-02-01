from django.db import models
import requests
from django.core.files import File
from django.urls import reverse


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', args=str([self.id]))


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('director_detail', args=str([self.id]))


class Writer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('writer_detail', args=str([self.id]))


class Genre(models.Model):
    genre_type = models.CharField(max_length=80)

    def __str__(self):
        return self.genre_type

    def get_absolute_url(self):
        return reverse('genre_type', args=str([self.id]))


class Type(models.Model):
    result_type = models.CharField(max_length=80)

    def __str__(self):
        return self.result_type

    def get_absolute_url(self):
        return reverse('result_type', args=str([self.id]))


class Rating(models.Model):
    source = models.CharField(max_length=120)
    value = models.CharField(max_length=60)

    def __str__(self):
        return self.source


class Movie(models.Model):
    Title = models.CharField(max_length=200, blank=True)
    Year = models.CharField(max_length=20, blank=True)
    Rated = models.CharField(max_length=30, blank=True)
    Released = models.CharField(max_length=30, blank=True)
    Runtime = models.CharField(max_length=30, blank=True)
    Genre = models.ManyToManyField(Genre, blank=True, null=True, related_name='movie_genre')
    Director = models.ManyToManyField(Director, blank=True, null=True, related_name='movie_director')
    Writer = models.ManyToManyField(Writer, blank=True, null=True, related_name='movie_writer')
    Actors = models.ManyToManyField(Actor, blank=True, null=True, related_name='movie_actor')
    Plot = models.TextField(max_length=2000, blank=True)
    Language = models.CharField(max_length=200, blank=True)
    Country = models.CharField(max_length=50, blank=True)
    Awards = models.CharField(max_length=200, blank=True)
    Poster = models.ImageField(upload_to="media/", blank=True)
    Poster_url = models.URLField(blank=True, null=True)
    Rating = models.ManyToManyField(Rating, blank=True, null=True, related_name='movie_rating')
    Metascore = models.CharField(max_length=25, blank=True)
    imbdRating = models.CharField(max_length=25, blank=True)
    imbdVotes = models.CharField(max_length=25, blank=True)
    imbdID = models.CharField(max_length=50, primary_key=True)
    Type = models.ForeignKey(Type, on_delete=models.SET_NULL, blank=True, null=True, related_name='movie_type')
    DVD = models.CharField(max_length=50, blank=True)
    BoxOffice = models.CharField(max_length=50, blank=True)
    Production = models.CharField(max_length=50, blank=True)
    Website = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.Title

    def save_poster_from_url(self):
        if self.Poster_url != '' and self.Poster == '':
            response = requests.get(self.Poster_url)
            image_file = File(response.content)
            self.Poster.save(self.Poster_url.split("/")[-1], image_file, save=True)
