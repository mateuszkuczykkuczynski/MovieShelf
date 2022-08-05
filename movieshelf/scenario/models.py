from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    social_media_link = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

