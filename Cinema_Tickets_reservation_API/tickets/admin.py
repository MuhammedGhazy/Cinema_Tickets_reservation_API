from django.contrib import admin
from . models import Movie, Guest, Reservations, Post
# Register your models here.
admin.site.register(Movie)
admin.site.register(Guest)
admin.site.register(Reservations)
admin.site.register(Post)