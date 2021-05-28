from enum import auto
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date 


class Like(models.Model):

    name = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100, default="Unknown")


class Post(models.Model):
    video = models.FileField(default = "default.mp4",upload_to="video/%y")
    name = models.CharField(max_length = 500)
    type = models.CharField(max_length = 500, default="Unknown")
    content = models.TextField(default="Unknown")
    rating = models.CharField(max_length=20, default="Unknown")
    # date_posted = models.DateTimeField(default=timezone.now)
    director = models.CharField(max_length=500, default="Unknown")
    cast = models.CharField(max_length=500, default="Unknown")
    country = models.CharField(max_length=500, default="Unknown")
    genres = models.TextField(max_length=500, default="Unknown")
    duration =models.CharField(max_length=500, default="Unknown")
    release_date = models.IntegerField()
    post_date = models.CharField(max_length=500, default=date.today().strftime("%d/%m/%Y"))
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class WatchLater(models.Model):
    user = models.CharField(max_length = 500, default="Unknown")
    name = models.CharField(max_length = 500)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

class Liked(models.Model):
    user = models.CharField(max_length = 500, default="Unknown")
    name = models.CharField(max_length = 500)
    type = models.CharField(max_length = 500, default="Unknown")
    content = models.TextField(default="Unknown")
    director = models.CharField(max_length=500, default="Unknown")
    cast = models.CharField(max_length=500, default="Unknown")
    country = models.CharField(max_length=500, default="Unknown")
    genres = models.TextField(max_length=500, default="Unknown")
    duration =models.CharField(max_length=500, default="Unknown")
    release_date = models.IntegerField()
    post_date = models.CharField(max_length=500, default=date.today().strftime("%d/%m/%Y"))
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})