from rest_framework import serializers
from .models import Guest, Movie, Reservations, Post

class MovieSerializers (serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReservitionSerializers (serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'

class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name', 'mobile']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
