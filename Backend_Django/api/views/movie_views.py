from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rate, Cluster, Profile,Movie_Cluster_Kmeans, Movie_Cluster_Hmeans, Movie_Cluster_EM
from api.serializers import MovieSerializer, Movie_Age_Serializer, Movie_Genre_Serializer
from rest_framework.response import Response
from django.db.models import Avg
import pandas as pd
import random, pprint

@api_view(['GET', 'POST', 'DELETE'])
def movies(request):
    if request.method == 'GET':
        id = request.GET.get('id', request.GET.get('movie_id', None))
        title = request.GET.get('title', None)
        movies = Movie.objects.all()
    
        if id:
            movies = movies.filter(pk=id)
        if title:
            movies = movies.filter(title__icontains=title)
        
        num = request.GET.get('num', None)
        canmore = True
        if len(movies) >= 12:
            if num:
                num = int(num)
                movies = movies[num*12:(num+1)*12]
                if len(movies) < 12:
                    canmore = False
            else:
                movies = movies[:12]
        else:
            canmore = False
        serializer = MovieSerializer(movies, many=True)
        return Response(data=[serializer.data, canmore], status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        movie = Movie.objects.all()
        movie.delete()
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        movies = request.data.get('movies', None)
        for movie in movies:
            id = movie.get('id', None)
            title = movie.get('title', None)
            genres = movie.get('genres', None)

            if not (id and title and genres):
                continue
            if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
                continue

            Movie(id=id, title=title, genres='|'.join(genres)).save()

        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def homepage(request):

    movies = Movie.objects.all().order_by('-watch_count')[:10]

    serializer = MovieSerializer(movies, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def genres(request):
    id = request.GET.get('id', request.GET.get('movie_id', None))
    title = request.GET.get('title', None)
    genre = request.GET.get('genre', None)
    watch_count = request.GET.get('watch_count', None)
    movies = Movie.objects.all().order_by('-watch_count')

    if id:
        movies = movies.filter(pk=id)
    if title:
        movies = movies.filter(title__icontains=title)
    if genre:
        movies = movies.filter(genres__icontains=genre)
    serializer = Movie_Genre_Serializer(movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def ages(request):
    age = request.GET.get('age', None)

    if age == "":
        print('여기떳다아아')
        age_index=""
    elif age == 'Under 18':
        age_index = 1
    elif age == "18-24":
        age_index = 18
    elif age == "25-34":
        age_index = 25
    elif age == "35-44":
        age_index = 35
    elif age == "45-49":
        age_index = 45
    elif age == "50-55":
        age_index = 50
    else:
        age_index = 56

    if age_index:
        profiles = Profile.objects.filter(age=age_index)
    else:
        profiles = Profile.objects.all()
    rates = Rate.objects.filter(UserID__in=profiles)
    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    rates = rates.order_by('-MovieID__watch_count')

    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def occupations(request):
    occupation = request.GET.get('occupation', None)

    if occupation:
        profiles = Profile.objects.filter(occupation=occupation)
    else:
        profiles = Profile.objects.all()
    rates = Rate.objects.filter(UserID__in=profiles)

    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    rates = rates.order_by('-MovieID__watch_count')
    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def genders(request):
    gender = request.GET.get('gender', None)

    if gender:
        profiles = Profile.objects.filter(gender=gender)
    else:
        profiles = Profile.objects.all()
    rates = Rate.objects.filter(UserID__in=profiles)
    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    rates = rates.order_by('-MovieID__watch_count')
    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie.watch_count += 1
    movie.save()
    cluster = Cluster.objects.get(pk=1)
    result = []
    serializer = MovieSerializer(movie)
    result.append(serializer.data)

    # H clustering
    if cluster.way == 'H':
        getMovie = Movie_Cluster_Hmeans.objects.get(MovieId=movie.id)
        if cluster.n_component == 3:
            lists = Movie_Cluster_Hmeans.objects.filter(H3=getMovie.H3)
        elif cluster.n_component == 4:
            lists = Movie_Cluster_Hmeans.objects.filter(H4=getMovie.H4)
        elif cluster.n_component == 5:
            lists = Movie_Cluster_Hmeans.objects.filter(H5=getMovie.H5)
        elif cluster.n_component == 6:
            lists = Movie_Cluster_Hmeans.objects.filter(H6=getMovie.H6)
        elif cluster.n_component == 7:
            lists = Movie_Cluster_Hmeans.objects.filter(H7=getMovie.H7)

    # Kmeans clustering
    if cluster.way == 'K':
        getMovie = Movie_Cluster_Kmeans.objects.get(MovieId=movie.id)
        if cluster.n_component == 3:
            lists = Movie_Cluster_Kmeans.objects.filter(K3=getMovie.K3)
        elif cluster.n_component == 4:
            lists = Movie_Cluster_Kmeans.objects.filter(K4=getMovie.K4)
        elif cluster.n_component == 5:
            lists = Movie_Cluster_Kmeans.objects.filter(K5=getMovie.K5)
        elif cluster.n_component == 6:
            lists = Movie_Cluster_Kmeans.objects.filter(K6=getMovie.K6)
        elif cluster.n_component == 7:
            lists = Movie_Cluster_Kmeans.objects.filter(K7=getMovie.K7)

    # EM clustering
    if cluster.way == 'EM':
        getMovie = Movie_Cluster_EM.objects.get(MovieId=movie.id)
        if cluster.n_component == 3:
            lists = Movie_Cluster_EM.objects.filter(EM3=getMovie.EM3)
        elif cluster.n_component == 4:
            lists = Movie_Cluster_EM.objects.filter(EM4=getMovie.EM4)
        elif cluster.n_component == 5:
            lists = Movie_Cluster_EM.objects.filter(EM5=getMovie.EM5)
        elif cluster.n_component == 6:
            lists = Movie_Cluster_EM.objects.filter(EM6=getMovie.EM6)
        elif cluster.n_component == 7:
            lists = Movie_Cluster_EM.objects.filter(EM7=getMovie.EM7)

    tmp = random.sample(list(lists), 5)
    for t in tmp:
        movie = Movie.objects.get(title=t.MovieId)
        serializer = MovieSerializer(movie)
        result.append(serializer.data)
    return Response(data=result, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def getarray(request):

    array = []

    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
                    'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
                    'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}

    movies = Movie.objects.all()
    movies_count = len(movies)

    for i in range(movies_count):
        tmp_array = [0]*19

        movie_genres = movies[i].genres.split('|')
        tmp_array[18] = movies[i].pk

        for j in range(len(movie_genres)):
            tmp_array[genre_number[movie_genres[j]]] = 1

        array.append(tmp_array)

    df = pd.DataFrame(array)
    df.to_csv("answer.csv", header=None, index=None)

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getrate(request, movie_id, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    movie = Movie.objects.get(pk=movie_id)
    rate = Rate.objects.filter(UserID=profile, MovieID=movie)

    if rate:
        result = {'flag':True, 'rate':rate[0].rating}
    else:
        result = {'flag':False}

    return Response(data=result, status=status.HTTP_200_OK)
