from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from api.serializers import UserSerializer, ProfileSerializer, MovieSerializer
from rest_framework.response import Response
from api.models import Profile, Cluster, Rate, Movie
from api.models import User_Cluster_Kmeans, User_Cluster_Hmeans, User_Cluster_EM
import random, pprint
import pandas as pd

@api_view(['GET', 'POST', 'DELETE'])
def users(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        # users = User.objects.all()[1:]

        if username:
            users = User.objects.filter(username__icontains=username)
        else:
            users = User.objects.all()[1:]
        # print(users)
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK)

    # if request.method == 'DELETE':
    #     movie = Movie.objects.all()
    #     movie.delete()
    #     return Response(status=status.HTTP_200_OK)

    # if request.method == 'POST':
    #     users = request.data.get('movies', None)
    #     for movie in movies:
    #         id = movie.get('id', None)
    #         title = movie.get('title', None)
    #         genres = movie.get('genres', None)
    #
    #         if not (id and title and genres):
    #             continue
    #         if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
    #             continue
    #
    #         Movie(id=id, title=title, genres='|'.join(genres)).save()
    #
    #     return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def detail(request, user_id):
    user = User.objects.get(pk=user_id)
    user_profile = Profile.objects.get(user=user)
    if request.method == 'GET':
        # 클러스터로 k, way 찾기
        clu = Cluster.objects.get(pk=1)
        k = clu.n_component
        way = clu.way
        clusters = []
        if way=="K":
            if(k==3):
                cluster_num = User_Cluster_Kmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].K3
                    clusters = User_Cluster_Kmeans.objects.filter(K3=cluster_num)
            elif(k==4):
                cluster_num = User_Cluster_Kmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].K4
                    clusters = User_Cluster_Kmeans.objects.filter(K4=cluster_num)
            elif(k==5):
                cluster_num = User_Cluster_Kmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].K5
                    clusters = User_Cluster_Kmeans.objects.filter(K5=cluster_num)
            elif(k==6):
                cluster_num = User_Cluster_Kmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].K6
                    clusters = User_Cluster_Kmeans.objects.filter(K6=cluster_num)
            else:
                cluster_num = User_Cluster_Kmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].K7
                    clusters = User_Cluster_Kmeans.objects.filter(K7=cluster_num)
        elif way=="H":
            if(k==3):
                cluster_num = User_Cluster_Hmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].H3
                    clusters = User_Cluster_Hmeans.objects.filter(H3=cluster_num)
            elif(k==4):
                cluster_num = User_Cluster_Hmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].H4
                    clusters = User_Cluster_Hmeans.objects.filter(H4=cluster_num)
            elif(k==5):
                cluster_num = User_Cluster_Hmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].H5
                    clusters = User_Cluster_Hmeans.objects.filter(H5=cluster_num)
            elif(k==6):
                cluster_num = User_Cluster_Hmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].H6
                    clusters = User_Cluster_Hmeans.objects.filter(H6=cluster_num)
            else:
                cluster_num = User_Cluster_Hmeans.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].H7
                    clusters = User_Cluster_Hmeans.objects.filter(H7=cluster_num)
        else:
            if(k==3):
                cluster_num = User_Cluster_EM.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].EM3
                    clusters = User_Cluster_EM.objects.filter(EM3=cluster_num)
            elif(k==4):
                cluster_num = User_Cluster_EM.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].EM4
                    clusters = User_Cluster_EM.objects.filter(EM4=cluster_num)
            elif(k==5):
                cluster_num = User_Cluster_EM.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].EM5
                    clusters = User_Cluster_EM.objects.filter(EM5=cluster_num)
            elif(k==6):
                cluster_num = User_Cluster_EM.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].EM6
                    clusters = User_Cluster_EM.objects.filter(EM6=cluster_num)
            else:
                cluster_num = User_Cluster_EM.objects.filter(UserID=user_id)
                if cluster_num:
                    cluster_num = cluster_num[0].EM7
                    clusters = User_Cluster_EM.objects.filter(EM7=cluster_num)
        profiles = []
        my_cluster = []
        serializer = ProfileSerializer(user_profile)
        my_cluster.append(serializer.data)
        if clusters:
            for i in range(0, len(clusters)):
                profiles.append(clusters[i].UserID)

            numbers = random.sample(range(0,len(profiles)), 5)
            for i in numbers:
                serializer = ProfileSerializer(profiles[i])
                my_cluster.append(serializer.data)
        # csv에 평점 데이터 유무 확인
        flag = False
        Users = pd.read_csv('./api/fixtures/user_rating.csv', header=0)
        Users = Users['user_pk']
        for user_pk in Users:
            if(user_pk==user_profile.pk):
                flag = True; break;
        my_cluster.append(flag)
        
        return Response(data=my_cluster, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user_profile.username = request.data.get('username', None)
        user_profile.age = request.data.get('age', None)
        user_profile.gender = request.data.get('gender', None)
        user_profile.occupation = request.data.get('occupation', None)
        user_profile.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def userMovie(request, user_id):
    user_profile = Profile.objects.get(user=user_id)
    movies = []
    rates = user_profile.profile_rate.all();
    cnt=0
    print(len(rates))
    for rate in rates:
        serializer = MovieSerializer(rate.MovieID)
        movies.append(serializer.data)
        cnt+=1;
        if cnt==10:
            break
    return Response(data = movies, status=status.HTTP_200_OK)