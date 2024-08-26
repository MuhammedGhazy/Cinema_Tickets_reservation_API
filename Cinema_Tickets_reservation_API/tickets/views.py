
from django.shortcuts import render
from django.http.response import JsonResponse 
from .models import Guest, Movie, Reservations, Post
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import GuestSerializers, MovieSerializers, ReservitionSerializers, PostSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets, filters
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . permission import IsAuthOrReadOnly
# Create your views here.
def no_rest_no_model (request):

    guest = [
        {
            'id': 1,
            'name': 'omar',
            'mobile': +20123456789,
        },
        {
            'id': 2,
            'name': 'hady',
            'mobile': +20129876543,
        }
    ]
    return JsonResponse(guest, safe=False)

def no_rest_from_model (request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

@api_view(['GET', 'POST'])
def FBV_LIST (request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializers = GuestSerializers(guests, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializers = GuestSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data, status= status.HTTP_201_CREATED)
        return Response (serializers.data, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])   
def FBV_pk (request, pk):

    try:
        guest = Guest.objects.get(pk = pk)
    except Guest.DoesNotExist:
        return Response (status= status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializers = GuestSerializers(guest)
        return Response(serializers.data)
    elif request.method == 'PUT':
        serializers = GuestSerializers(guest, data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data, status= status.HTTP_202_ACCEPTED)
        return Response (serializers.errors, status= status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        guest.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
class CBV_List(APIView):
    def get (self, request):
        guests = Guest.objects.all()
        serializers = GuestSerializers(guests, many = True)
        return Response(serializers.data)
    def post(self, request):
        serializers = GuestSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data, status = status.HTTP_201_CREATED)
        return Response (serializers.data, status = status.HTTP_400_BAD_REQUEST)

class CBV_pk (APIView):
    def get_object (self, pk):
        try:
            return Guest.objects.get(pk = pk)
        except Guest.DoesNotExist():
            raise Http404
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializers = GuestSerializers(guest)
        return Response (serializers.data)
    def put (self, request, pk):
        guest = self.get_object(pk)
        serializers = GuestSerializers(guest, data= request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)
    def delete (self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response (status= status.HTTP_204_NO_CONTENT)

class mixins_List(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

class mixins_pk(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
   # permission_classes = [IsAuthenticated]
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
class viewsets_guest (viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

class view_sets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends =[filters.SearchFilter]
    search_fields = ['movie']

class view_sets_reservation(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservitionSerializers

@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializers = MovieSerializers(movies, many = True)
    return Response (serializers.data, status = status.HTTP_302_FOUND)

@api_view(['POST'])
def new_reservation (request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
        #d_t = request.data['date_time'],
        )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data ['mobile']
    guest.save()

    reservations = Reservations()
    reservations.guest = guest
    reservations.movie = movie
    reservations.save()

    return Response(request.data, status= status.HTTP_201_CREATED)

class Post_pk (generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
