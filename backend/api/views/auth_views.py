from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import create_profile, Profile, User, Movie, Rate
from api.serializers import ProfileSerializer
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import csv, copy, pprint
import pandas as pd
import numpy as np
from api.models import User_Cluster_Kmeans, User_Cluster_Hmeans, User_Cluster_EM


genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
                    'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
                    'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}

@api_view(['POST'])
def signup_many(request):
  print("회원가입!")
  if request.method == 'POST':
      profiles = request.data.get('profiles', None)
      for profile in profiles:
          username = profile.get('username', None)
          password = profile.get('password', None)
          age = profile.get('age', None)
          occupation = profile.get('occupation', None)
          gender = profile.get('gender', None)

          create_profile(username=username, password=password, age=age,
                          occupation=occupation, gender=gender)

      return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def signup(request):
  if request.method == 'POST':
      name = request.data.get('username', None)
      if(User.objects.filter(username=name)):
        return Response(data=False, status=status.HTTP_201_CREATED)
        
      age = request.data.get('age', None)
      gender = request.data.get('gender', None)
      occupation = request.data.get('occupation', None)
      password = request.data.get('password')
      create_profile(username=name, password=password, age=age, occupation=occupation, gender=gender)

      return Response(data=True, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            data = {'user': username, 'id_number':user.id, 'admin':user.is_superuser}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'user': '', 'admin':False}
            return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def userstate(request):
    if request.user.is_authenticated:
        user = request.user
        data = {'user': user.username}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {'user': ''}
        return Response(data=data, status=status.HTTP_200_OK)

@login_required
def logout(request):
    user = request.user
    auth_logout(request)
    return Response(status=status.HTTP_200_OK)

def create_User():
  Users = pd.read_csv('./api/fixtures/user_rating.csv', header=0)
  users_pk = Users['user_pk']
  Users = Users[genre_number.keys()]
  return Users, users_pk
# 유저간의 거리 계산
def distance_user(input_user_score, user_score):
  dis = np.linalg.norm(input_user_score-user_score)
  return dis
# 가장 가까운 유저 출력
def find_near_user(users):
  near_user = min(users)
  idx = users.index(near_user)
  return idx
# user_rating.csv에 데이터 추가하기
def add_user_rating(scores, pk):
  fields = copy.deepcopy(scores)
  fields.append(pk)
  f = open('./api/fixtures/user_rating.csv', 'a', encoding='utf-8', newline='')
  wr = csv.writer(f)
  wr.writerow(fields)
  f.close()
# K, H, EM 클러스터링!(K3~K7, H3~H7, EM3~EM7 저장하기)
def CheckCluster(Nearest, input_data):
  K_list = [0,0,0,0,0]; H_list = [0,0,0,0,0]; EM_list = [0,0,0,0,0]; 
  table = [[[0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]],
           [[0,0,0],
           [0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0,0]],
           [[0,0,0],
           [0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0,0],
           [0,0,0,0,0,0,0]]];
  for profile in Nearest:
    K_clusters = profile.user_cluster_Kmeans.all()[0]
    H_clusters = profile.user_cluster_Hmeans.all()[0]
    EM_clusters = profile.user_cluster_EM.all()[0]
    # K
    table[0][0][(K_clusters.K3)] += 1;
    table[0][1][(K_clusters.K4)] += 1;
    table[0][2][(K_clusters.K5)] += 1;
    table[0][3][(K_clusters.K6)] += 1;
    table[0][4][(K_clusters.K7)] += 1;
    # H
    table[1][0][(H_clusters.H3)] += 1;
    table[1][1][(H_clusters.H4)] += 1;
    table[1][2][(H_clusters.H5)] += 1;
    table[1][3][(H_clusters.H6)] += 1;
    table[1][4][(H_clusters.H7)] += 1;
    # EM
    table[2][0][(EM_clusters.EM3)] += 1;
    table[2][1][(EM_clusters.EM4)] += 1;
    table[2][2][(EM_clusters.EM5)] += 1;
    table[2][3][(EM_clusters.EM6)] += 1;
    table[2][4][(EM_clusters.EM7)] += 1;
  for j in range(2):
    if j==0:
      for i in range(5):
        K_list[i] = table[0][i].index(max(table[0][i]))
    elif j==1:
      for i in range(5):
        H_list[i] = table[1][i].index(max(table[1][i]))
    else:
      for i in range(5):
        EM_list[i] = table[2][i].index(max(table[2][i]))

  User_Cluster_Kmeans(UserID=input_data,
    K3=K_list[0], K4=K_list[1], K5=K_list[2], 
    K6=K_list[3], K7=K_list[4]).save()
  User_Cluster_Hmeans(UserID=input_data, 
    H3=H_list[0], H4=H_list[1], H5=H_list[2], 
    H6=H_list[3], H7=H_list[4]).save()
  User_Cluster_EM(UserID=input_data, 
    EM3=EM_list[0], EM4=EM_list[1], EM5=EM_list[2], 
    EM6=EM_list[3], EM7=EM_list[4]).save()

@api_view(['POST'])
def new_cluster(request):
  if request.method == 'POST':
    Users, users_pk = create_User()
    user = request.data.get('user_pk')
    
    flag = False
    Users = pd.read_csv('./api/fixtures/user_rating.csv', header=0)
    Users = Users['user_pk']
    for user_pk in Users:
      if(user_pk==user):
        flag = True; break;
    if(flag): return Response(data=1, status=status.HTTP_200_OK)
    elif(user==""): return Response(data=0, status=status.HTTP_200_OK)
    movies = request.data.get('movies')
    profile = Profile.objects.get(user=user)

    rate_genre_sum = [0 for i in range(18)]
    rate_genre_cnt = [0 for i in range(18)]
    rate_genre = [0 for i in range(18)]
    
    for key, val in movies.items():
      key = int(key)
      val = float(val)
      Rate(UserID=profile,MovieID=Movie.objects.get(pk=key),rating=val,Timestamp=0).save()
      genres = Movie.objects.get(pk=key).genres.split("|")
      for genre in genres:
        num = genre_number[genre]
        rate_genre_sum[num] += val
        rate_genre_cnt[num] += 1
    for i in range(18):
      if(rate_genre_cnt[i]==0): continue
      rate_genre[i] = round(rate_genre_sum[i]/rate_genre_cnt[i], 2)
    add_user_rating(rate_genre, user)

    users_distance = []; # 유저간의 거리 리스트
    rate_genre = np.array(rate_genre)
    for user_score, user_pk in zip(Users.values, users_pk):
      dis = distance_user(rate_genre, user_score)
      users_distance.append(dis)

    Nearest_user = [] # 가장 가까운 유저 리스트 7개
    for i in range(7):
      idx = find_near_user(users_distance)
      Nearest_user.append(Profile.objects.get(user=idx+2))
      users_distance[idx] = 100
    print(Nearest_user)
    CheckCluster(Nearest_user, profile)
    return Response(data=2, status=status.HTTP_200_OK)