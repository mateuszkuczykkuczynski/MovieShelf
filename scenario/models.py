from django.db import models
import requests
from django.core.files import File
from django.urls import reverse
from io import BytesIO
from django.core import files
from django.utils.text import slugify
from members.models import UserProfile

from django.core.files import File  # you need this somewhere
import urllib
import os


class Actor(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', args=[self.slug])


class Director(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('director_detail', args=[self.slug])


class Writer(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('writer_detail', args=[self.slug])


class Genre(models.Model):
    genre_type = models.CharField(max_length=80)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None:
            self.slug = slugify(self.genre_type)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.genre_type

    def get_absolute_url(self):
        return reverse('genre_type', args=[self.slug])


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
    Genre = models.ManyToManyField(Genre, blank=True, related_name='movie_genre')
    Director = models.ManyToManyField(Director, blank=True, related_name='movie_director')
    Writer = models.ManyToManyField(Writer, blank=True, related_name='movie_writer')
    Actors = models.ManyToManyField(Actor, blank=True, related_name='movie_actor')
    Plot = models.TextField(max_length=2000, blank=True)
    Language = models.CharField(max_length=200, blank=True)
    Country = models.CharField(max_length=50, blank=True)
    Awards = models.CharField(max_length=200, blank=True)
    Poster = models.ImageField(max_length=500, upload_to='posters', blank=True)
    Poster_url = models.URLField(max_length=500, blank=True, null=True)
    Rating = models.ManyToManyField(Rating, blank=True, related_name='movie_rating')
    Metascore = models.CharField(max_length=25, blank=True)
    imdbRating = models.CharField(max_length=25, blank=True)
    imdbVotes = models.CharField(max_length=25, blank=True)
    imdbID = models.CharField(max_length=50, primary_key=True)
    Type = models.CharField(max_length=500, blank=True, null=True)
    DVD = models.CharField(max_length=50, blank=True)
    BoxOffice = models.CharField(max_length=50, blank=True)
    Production = models.CharField(max_length=50, blank=True)
    Website = models.CharField(max_length=500, blank=True)
    totalSeasons = models.CharField(max_length=30, blank=True)
    WebsiteUsersRating = models.ManyToManyField(UserProfile, through='MovieShelfRating')

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('movie_details', args=[self.imdbID])

    # @property
    # def average_rating(self):
    #     shelf_ratings = self.WebsiteUsersRating.all()
    #     if shelf_ratings:
    #         return sum(rating.rating for rating in shelf_ratings) / len(shelf_ratings)
    #     else:
    #         return None

    def save(self, *args, **kwargs):
        if self.Poster == '' and self.Poster_url != '':
            resp = requests.get(self.Poster_url)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.Poster_url.split("/")[-1]
            self.Poster.save(file_name, files.File(pb), save=False)

        return super().save(*args, **kwargs)
        # if self.Poster_url != '' and self.Poster == '':
        #     response = requests.get(self.Poster_url)
        #     image_file = File(response.content)
        #     self.Poster.save(self.Poster_url.split("/")[-1], image_file, save=True)


class WatchedByUser(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='watched_by_user')
    watched = models.ManyToManyField(Movie, related_name='watched_position')


class ToWatchByUser(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='to_watch_by_user')
    to_watch = models.ManyToManyField(Movie, related_name='position_to_watch')


class MovieShelfRating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='users_rating')
    position = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='website_rating')
    rating = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'position'], name='unique_ratings')
        ]
