from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance
    
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance
    
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'genres', 'uuid')

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('title', 'description', 'movies')

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        return collection
    
    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies')
        movies = instance.movies.all()
        movies = list(movies)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        for movie_data in movies_data:
            movie_id = movie_data.get('uuid', None)
            if movie_id:
                movie = Movie.objects.get(uuid=movie_id)
                movie.title = movie_data.get('title', movie.title)
                movie.genres = movie_data.get('genres', movie.genres)
                movie.description = movie_data.get('description', movie.description)
                movie.save()
                movies.remove(movie)
            else:
                movie = Movie.objects.create(collection=instance, **movie_data)

        for movie in movies:
            movie.delete()

        return instance
    
    

