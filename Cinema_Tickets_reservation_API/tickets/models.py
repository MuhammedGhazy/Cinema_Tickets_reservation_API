from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Movie (models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.hall} ({self.movie})"


class Guest (models.Model):
    name = models.CharField(max_length=20)
    mobile = models.IntegerField()

    def __str__(self):
        return self.name 

class Reservations (models.Model):
    guest = models.ForeignKey(Guest, related_name= 'reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name= 'reservation', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.guest} ({self.movie})"


class Post (models.Model):
    auth = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def Token_Created(sender, instance, created, **kwrgs):
    if created:
        Token.objects.create(user = instance)
    