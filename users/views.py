import datetime
import coreapi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from sqlalchemy import String
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import requests
from rest_framework import status
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from django.core.cache import cache
from django.core.cache import cache
from .factory import *
from requests.auth import HTTPBasicAuth
import os
from apiproject.utils import generate_payload, get_token


class PopulateView(APIView):
    
    def get(self, request):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            
            user_factory = UserFactory.build()
            unhashed_password = user_factory.password
            print("USERNAME --->  ", user_factory.username)
            print("PASSWORD --->  ", unhashed_password)
            user_factory.set_password(unhashed_password)
            user_factory.save()
            for i in range(1):
                collection_factory = CollectionFactory.build(user=user_factory)
                collection_factory.save()
                for j in range(2):
                    movie_factory = MovieFactory.build(collection=collection_factory)
                    movie_factory.save()
            
            return Response({'message':'data populated'})
        else:
            raise AuthenticationFailed('Unauthenticated')
        
        
        
        
        
class RequestCountMixin:
    def get_request_count(self):
        return cache.get('request_counter', default=0)
    
    
    

class ListAllUsers(APIView):
    def get(self, request):
        payload = get_token(request)
        print(payload)
        if payload:
            users = User.objects.all()
            serializer = UserListSerializer(users, many = True)
            return Response(serializer.data)
        return Response({'error':'login first'})
    
    
    

class CreateUserView(RequestCountMixin,APIView):
    def post(self, request):
        
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
    
    

class Register(RequestCountMixin,APIView):

    def post(self, request):
        
        payload = generate_payload(request)

        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        
        response.set_cookie(key = 'access_token', value=token, httponly=True)
        response.data={
            'access_token':token,
        }
        return response
    
    
    
class UserView(RequestCountMixin,APIView):
    def get(self, request):
        
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
    

class LogoutView(RequestCountMixin, APIView):
    def post(Self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.data={
            'message':'Success'
        }
        return response
    


class MovieList(RequestCountMixin,APIView):
    
    
    def get(self, request, format=None):
        
        disable_warnings(InsecureRequestWarning)
        url = 'https://demo.credy.in/api/v1/maya/movies/'
        
        username = os.environ.get('MOVIE_USERNAME')
        password = os.environ.get('MOVIE_PASSWORD')
        
        auth = HTTPBasicAuth(username, password)
        
        
        try:
            response = requests.get(url, verify=False, auth = auth)
            
            if response.status_code == 200:
                data = response.json()
                
                movies = data['results']

                serialized_movies = []
                for movie in movies:
                    serialized_movies.append({
                        'title': movie['title'],
                        'description': movie['description'],
                        'genres': ', '.join(movie['genres']) if 'genres' in movie else '',
                        'uuid': movie['uuid']
                    })
                
                return Response(serialized_movies)
            
            elif response.status_code == 401:
                return Response({"message":"Authentication failed"})
            
        except request.exceptions.ResuestEXception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionView(RequestCountMixin, APIView):

    serializer_class = CollectionSerializer
    def get(self, request):

        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        
        if user is None:
            return Response({'message':'register to view the collections'})
        

        collections = user.collections.all()
        favourite_genres = user.get_favourite_genres()
        data = {
            "collections": [],
            "favourite_genres": favourite_genres
        }
        for collection in collections:
            collection_data = {
                "title": collection.title,
                "uuid": collection.uuid,
                "description": collection.description
            }
            data["collections"].append(collection_data)
        response_data = {
            "is_success": True,
            "data": data
        }
        return Response(response_data)
    
    def post(self, request):
        
        collection_serializer = CollectionSerializer(data=request.data)
        
        if collection_serializer.is_valid():
            payload = get_token(request)
            user =User.objects.filter(id = payload['id']).first()
        
            collection_serializer.save(user=user) 
            
            return Response({"collection_uuid": collection_serializer.instance.uuid}, status=status.HTTP_201_CREATED)
        else:
            return Response(collection_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CollectionDetailView(RequestCountMixin,APIView):

    def get(self, request, collection_uuid):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            try:
                collection = Collection.objects.get(uuid=collection_uuid)
                movies = collection.movies.all()  
                data = {
                    'title': collection.title,
                    'description': collection.description,
                    'movies': [
                        {
                            'title': movie.title,
                            'description': movie.description,
                            'genres': movie.genres,
                            'uuid':movie.uuid,
                        } for movie in movies
                    ]
                }
                
                return Response(data)
            except Collection.DoesNotExist:
                return Response({"message":"Collection does not exist"},status=status.HTTP_404_NOT_FOUND)
        else:
            raise AuthenticationFailed('Unauthenticated')
        
        
    def put(self, request, collection_uuid):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            try:
                collection = Collection.objects.get(uuid=collection_uuid)
            except:
                return Response({"error": "Collection matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CollectionSerializer(collection, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            raise AuthenticationFailed('Unauthenticated')
        
        
    def delete(self, request, collection_uuid):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            
            collection = get_object_or_404(Collection, uuid=collection_uuid)
            
            collection.delete()
            return Response({'message':'collection deleted'},status=status.HTTP_204_NO_CONTENT)
        
        else:
            raise AuthenticationFailed('Unauthenticated')


class CountRequestView(APIView):
    def get(self, request):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            request_count = cache.get('request_counter', default=0)
            return Response({'requests': request_count})
        else:
            raise AuthenticationFailed('Unauthenticated')
        
    
    
    
class ResetCountRequestVIew(APIView):
    def post(self, request):
        payload = get_token(request)
        user =User.objects.filter(id = payload['id']).first()
        if user:
            cache.set('request_counter', 0)
            
            return Response({'message': 'Request count reset successfully'})
        else:
            raise AuthenticationFailed('Unauthenticated')
        