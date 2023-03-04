from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.contrib.auth.models import UserManager
from collections import Counter

class User(AbstractBaseUser):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    

    objects = UserManager()
    
    def get_favourite_genres(self):
        genre_counts = Counter()
        for collection in self.collections.all():
            for movie in collection.movies.all():
                genre_counts[movie.genres] += 1
        return ', '.join(genre for genre, count in genre_counts.most_common(3))

class Collection(models.Model):
    title = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, related_name = 'collections', on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=15)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField( default='SOME STRING')
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title