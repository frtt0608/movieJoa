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
        # cnt = int(request.GET.get('cnt'))
        # print(cnt)

        movies = Movie.objects.all()
        # pprint.pprint(movies)

        if id:
            movies = movies.filter(pk=id)

        if title:
            movies = movies.filter(title__icontains=title)
        # else:
        #     movies = Movie.objects.all()[cnt-10:cnt]
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

    # 1. 해당 나이에 포함된 모든 사람들
    if age_index:
        profiles = Profile.objects.filter(age=age_index)
    else:
        profiles = Profile.objects.all()
    # 2. 해당 사람들이 남긴 모든 댓글들
    rates = Rate.objects.filter(UserID__in=profiles)

    # 3. 해당 영화들의 평점들을 annotate 잘 시킴.
    # rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count').annotate(Avg('rating'))
    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    # rates = rates.order_by('-rating__avg')
    rates = rates.order_by('-MovieID__watch_count')

    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def occupations(request):
    occupation = request.GET.get('occupation', None)

    # 1. 해당 직업에 포함된 모든 사람들
    if occupation:
        profiles = Profile.objects.filter(occupation=occupation)
    else:
        profiles = Profile.objects.all()
    # 2. 해당 사람들이 남긴 모든 댓글들
    rates = Rate.objects.filter(UserID__in=profiles)

    # 3. 해당 영화들의 평점들을 annotate 잘 시킴.
    # rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count').annotate(Avg('rating'))
    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    # rates = rates.order_by('-rating__avg')
    rates = rates.order_by('-MovieID__watch_count')

    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def genders(request):
    gender = request.GET.get('gender', None)

    # 1. 해당 직업에 포함된 모든 사람들
    if gender:
        profiles = Profile.objects.filter(gender=gender)
    else:
        profiles = Profile.objects.all()
    # 2. 해당 사람들이 남긴 모든 댓글들
    rates = Rate.objects.filter(UserID__in=profiles)

    # 3. 해당 영화들의 평점들을 annotate 잘 시킴.
    # rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count').annotate(Avg('rating'))
    rates = rates.values('MovieID', 'MovieID__title', 'MovieID__genres', 'MovieID__watch_count', 'MovieID__plot', 'MovieID__url', 'MovieID__director', 'MovieID__casting').annotate(Avg('rating'))
    # rates = rates.order_by('-rating__avg')
    rates = rates.order_by('-MovieID__watch_count')

    serializer = Movie_Age_Serializer(rates, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def detail(request, movie_id):
    # pprint.pprint(request.data)
    movie = Movie.objects.get(pk=movie_id)
    movie.watch_count += 1
    movie.save()
    cluster = Cluster.objects.get(pk=1)
    result = []
    serializer = MovieSerializer(movie)
    # rate = Rate.objects.get(UserID)
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

    ## 1. 변수 정의
    # 1-1. array : array 에 있는 데이터를 csv로 변환할 것입니다.
    # 예시 array[0] = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Toy Story (1995)']
    # toy story라는 영화는 0011100000000000이라는 장르데이터를 가진다는 것을 의미합니다.

    # 하나의 영화가 어떠한 장르를 포함하는지 0, 1로 표시할 것이며 행에는 하나의 영화 데이터를 넣을 것입니다.
    # 열에는 장르 이름을 의미합니다.
    array = []

    # 1-2. genre_number: array에 들어가는 장르의 인덱스입니다. ( 열 ) / 총 19개(18+영화이름넣을공간1) 입니다.
    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
                    'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
                    'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}

    ## 2. array 만들기
    # 2-1. 전체 영화를 가져오고, 총 몇개의 영화인지 확인합니다.
    movies = Movie.objects.all()
    # last_movie_id = movies[len(movies)-1].id
    movies_count = len(movies)

    # 2-2. 하나의 영화데이터를 tmp_array 에 담아서 array로 보내기.
    for i in range(movies_count):
        tmp_array = [0]*19

        movie_genres = movies[i].genres.split('|')
        tmp_array[18] = movies[i].pk

        for j in range(len(movie_genres)):
            tmp_array[genre_number[movie_genres[j]]] = 1

        array.append(tmp_array)

    # 2-3. csv 파일로 array 를 저장하자.
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
