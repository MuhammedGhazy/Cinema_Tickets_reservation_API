"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guest', views.viewsets_guest)
router.register('movie', views.view_sets_movie)
router.register('reserv', views.view_sets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/jsonresponsenomodel/', views.no_rest_no_model),
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),
    path('rest/fbvlist/', views.FBV_LIST),
    path('rest/fbvlist/<int:pk>/', views.FBV_pk),
    path('rest/CBV/', views.CBV_List.as_view()),
    path('rest/CBV/<int:pk>', views.CBV_pk.as_view()),
    path('rest/mixins/', views.mixins_List.as_view()),
    path('rest/mixins/<int:pk>/', views.mixins_pk.as_view()),
    path('rest/generics/', views.generics_list.as_view()),
    path('rest/generics/<int:pk>/', views.generics_pk.as_view()),
    path('rest/viewsets/', include(router.urls)),
    path('rest/viewsets/', include(router.urls)),
    path('rest/viewsets/', include(router.urls)),
    path('fbv/findmovie/', views.find_movie),
    path('fbv/new_reservation/', views.new_reservation),
    path('api-auth', include('rest_framework.urls')),
    path('obtain-auth-token', obtain_auth_token),
    path('post/generics/<int:pk>/', views.Post_pk.as_view()),
]