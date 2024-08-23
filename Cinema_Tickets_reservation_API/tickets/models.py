from django.db import models

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