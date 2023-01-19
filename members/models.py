from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE, related_name='profiles')
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)
    socials = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])


