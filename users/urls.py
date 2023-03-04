from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    
    path('',MovieList.as_view() ),
    path('create-user/',CreateUserView.as_view() ),
    path('request-count/',CountRequestView.as_view() ),
    path('request-count/reset/',ResetCountRequestVIew.as_view() ),
    path('register/',Register.as_view() ),
    path('user/',UserView.as_view() ),
    path('logout/',LogoutView.as_view() ),
  
    path('collection/',CollectionView.as_view() ),
    path('collection/<uuid:collection_uuid>/',CollectionDetailView.as_view() ),
    path('listusers/',ListAllUsers.as_view() ),
    path('populate/',PopulateView.as_view() ),

]
