import factory

from .models import *
import factory
from .models import Collection, Movie



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    username = factory.Faker('user_name')
    password = factory.Faker('password')

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Sequence(lambda n: f'Collection {n}')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Sequence(lambda n: f'Movie {n}')
    genres = factory.Faker('text')
    description = factory.Faker('text')
    collection = factory.SubFactory(CollectionFactory)
    
    
