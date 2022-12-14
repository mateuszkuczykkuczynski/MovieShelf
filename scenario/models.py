from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import requests
from io import BytesIO
from django.core import files


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    social_media_link = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('homepage')


class Actor(models.Model):
    name = models.CharField(max_length=80, unique=True)
    picture = models.ImageField(blank=True)
    slug = models.SlugField(null=True, unique=True)
    movies = models.ManyToManyField('scenario.Movie')

    def get_absolute_url(self):
        return reverse('actors', args=[self.slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Genre(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('genres', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.title.replace(" ", "")
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Rating(models.Model):
    source = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.source


class Movie(models.Model):
    Title = models.CharField(max_length=1000)
    Year = models.CharField(max_length=25, blank=True)
    Rated = models.CharField(max_length=10, blank=True)
    Released = models.CharField(max_length=25, blank=True)
    Runtime = models.CharField(max_length=25, blank=True)
    Genre = models.ManyToManyField(Genre, blank=True)
    Director = models.CharField(max_length=1000, blank=True)
    Writer = models.CharField(max_length=1000, blank=True)
    Actors = models.ManyToManyField(Actor, blank=True)
    Plot = models.CharField(max_length=900, blank=True)
    Language = models.CharField(max_length=1000, blank=True)
    Country = models.CharField(max_length=1000, blank=True)
    Awards = models.CharField(max_length=1000, blank=True)
    Poster = models.ImageField(upload_to='movies', blank=True)
    Poster_url = models.URLField(blank=True)
    Ratings = models.ManyToManyField(Rating, blank=True)
    Metascore = models.CharField(max_length=5, blank=True)
    imdbRating = models.CharField(max_length=5, blank=True)
    imdbVotes = models.CharField(max_length=100, blank=True)
    imdbID = models.CharField(max_length=100, blank=True)
    Type = models.CharField(max_length=10, blank=True)
    DVD = models.CharField(max_length=25, blank=True)
    BoxOffice = models.CharField(max_length=25, blank=True)
    Production = models.CharField(max_length=100, blank=True)
    Website = models.CharField(max_length=150, blank=True)
    totalSeasons = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if self.Poster == '' and self.Poster_url != '':
            resp = requests.get(self.Poster_url)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.Poster_url.split("/")[-1]
            self.Poster.save(file_name, files.File(pb), save=False)

        return super().save(*args, **kwargs)
