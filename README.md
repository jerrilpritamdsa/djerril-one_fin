# djerril-one_fin


# Problem statement

1.) Integration with an API which serves a list of movies and their genres

2.) Use the API to list movies for the users of your web application. 
They should be able to see the list of movies and add any movie which they like into their collections. 
Each user can create multiple collections and multiple movies into the collections. Develop APIs for this application per specification below. No frontend is required to be developed.

3.) We also want to have a monitoring system of counting the number of requests done to your project. 
Write a custom middleware for counting all requests coming to your server too, and an API to monitor it too.


__________________________________________________________________________________________________________________________

# Solution(scalable)

I have used postman for the documentaion. 

Kindly refer to README file for more info


https://documenter.getpostman.com/view/24391840/2s93JnUmg3



There also was technical difficulties with deployment using vercel.
and it is causing errors due to redis connectivity

https://djerril-one-fin-6nqf-7xoue5mvg-jerrilpritamdsa.vercel.app/#

# Here are the endpoints and its responses

1.)  GET   localhost:8000/movies/

This gives the paginated movies using 3rd party api at
https://demo.credy.in/api/v1/maya/movies/

It uses a Basic auth authentication and the userid and password are obtained from .env file similar to
obtaining some of the setting configurations 

![image](https://user-images.githubusercontent.com/63163179/222934216-f8297ef2-875f-464c-a23b-db2dfec29267.png)

__________________________________________________________________________________________________________________________

2.)   POST   localhost:8000/create-user/

This endpoint helps to create a user 

![image](https://user-images.githubusercontent.com/63163179/222934284-1eaefd6d-c91d-48d5-9cd3-fcf6f26bbad2.png)

__________________________________________________________________________________________________________________________


3.)  POST  localhost:8000/register/

This endpoint helps to login the created user from step 2.
Provides with a JWT access token WHICH IS STORED IN COOKIE and is retrieved for authentication of that user

![image](https://user-images.githubusercontent.com/63163179/222934347-2bbf2006-2ca0-4cae-810b-7663631a8baf.png)

__________________________________________________________________________________________________________________________


4.)  GET, POST   localhost:8000/collection/

This endpoint is used to get all the collections associated with that user and also post new collections.
This also provides with favourite genres of that user

![image](https://user-images.githubusercontent.com/63163179/222934375-2ee2c385-cbfa-4b39-8250-be9e4163bb5d.png)
![image](https://user-images.githubusercontent.com/63163179/222934391-ca7a8a13-3d69-49a0-97fc-25527a955740.png)

__________________________________________________________________________________________________________________________


5.) GET, POST, PUT, DELETE   localhost:8000/collection/:collection_id/

this takes in unique id of the collection that was generated when it was created and we can perform CRUD operations
![image](https://user-images.githubusercontent.com/63163179/222934487-4183944f-d997-4490-9a56-e0e2c4673127.png)

__________________________________________________________________________________________________________________________


6.)  GET localhost:8000/request-count/
this endpoint responds with total number of requests made with the help of REDIS CLIENT-SIDE CACHING.
this is intigrated with DJNAGO CUSTOM MIDDLEWARE
![image](https://user-images.githubusercontent.com/63163179/222934535-80a8cbc6-e510-49f2-84ee-b4cfa526712d.png)

__________________________________________________________________________________________________________________________


7.) POST localhost:8000/request-count/reset/
this endpoint is used to reset the cache data to remove all the request counts and set it to zero
![image](https://user-images.githubusercontent.com/63163179/222934576-d9713851-b057-4937-a897-d416026a46bd.png)

__________________________________________________________________________________________________________________________


8.) GET localhost:8000/populate/
This endpoint is used to populate the database using FACTORY BOY 
as an example it creates one user , one collection of that user and two movies associated with that collection

__________________________________________________________________________________________________________________________


9.) GET   localhost:8000/listusers/
This endpoint is used to list all the users that were created which only admin can have access to view
![image](https://user-images.githubusercontent.com/63163179/222934720-1d7c4803-2c0a-47e3-9b75-e3d0df0e48de.png)

__________________________________________________________________________________________________________________________















