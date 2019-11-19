import pandas as pd
import numpy as np
import pprint, random, csv, copy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from api.models import Movie, Cluster, Profile
from api.models import Movie_Cluster_Kmeans, Movie_Cluster_Hmeans, Movie_Cluster_EM
from api.models import User_Cluster_Kmeans, User_Cluster_Hmeans, User_Cluster_EM

from sklearn.cluster import KMeans # KM_cluster
from sklearn.mixture import GaussianMixture  # EM_cluster
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.cluster import AgglomerativeClustering # H_cluster

label = ["Action","Adventure","Animation","Children's",
                "Comedy","Crime","Documentary","Drama","Fantasy",
                "Film-Noir","Horror","Musical","Mystery","Romance",
                "Sci-Fi","Thriller","War","Western"]

# # # # # # # # # # # # # # # # ## # # # # # Movie KNN # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 새로운 영화 저장하기
def new_movie(request):
  title = request.data.get('title')
  genres = request.data.get('genres')
  plot = request.data.get('plot', None)
  url = request.data.get('url', None)
  director = request.data.get('director', None)
  casting = request.data.get('casting', None)
  Movie(title=title, genres='|'.join(genres), plot=plot, url=url, director=director, casting='|'.join(casting)).save()

# 영화간의 거리 계산(장르, 감독, 배우)
def distance_movie(input_movie, input_movie_genre, movie_genre, movie_pk):
  movie = Movie.objects.get(pk=movie_pk)
  dist = np.linalg.norm(input_movie_genre - movie_genre)
  for genre in movie.genres.split("|"):
    if genre in input_movie.genres.split("|"):
      dist -= -0.1
  for cast in movie.casting.split("|"):
    if cast in input_movie.casting.split("|"):
      dist -= 0.1
  if movie.director == input_movie.director:
    dist -= 0.1
  return dist
# 가장 가까운 영화 출력
def find_near_movie(movie):
  near_movie = min(movie)
  idx = movie.index(near_movie)
  return idx
# 영화 데이터 가져오기
def create_Movie():
  Movies = pd.read_csv('./api/fixtures/movie_genre.csv', header=0)
  movies_pk = Movies['movie_pk']
  Movies = Movies[label]
  Movies.head()
  return Movies, movies_pk

@api_view(['GET','POST'])
def KNN_algorithm_movie(request):
  new_movie(request)
  input_movie = Movie.objects.all().last()
  input_movie_genre = [0 for i in range(len(label))];

  for genre in input_movie.genres.split("|"):
    idx = label.index(genre)
    input_movie_genre[idx] = 1

  Movies, movies_pk = create_Movie()
  dist_movie = [0 for i in range(movies_pk.values[-1]+1)] # 영화간의 거리 리스트
  input_movie_genre = np.array(input_movie_genre)
  for movie_genre, movie_pk in zip(Movies.values, movies_pk):
    temp = distance_movie(input_movie, input_movie_genre, movie_genre, movie_pk)
    dist_movie[movie_pk] = temp # 거리 저장.

  Nearest_movie = [] # 가장 가까운 영화 리스트 7개
  for i in range(7):
    idx = find_near_movie(dist_movie)
    Nearest_movie.append(idx)
    dist_movie[idx] = 100
  print(Nearest_movie)
  target = "MOVIE"
  CheckCluster(Movies, Nearest_movie, input_movie, target)
  return Response(status=status.HTTP_200_OK)

# K, H, EM 클러스터링!(K3~K7, H3~H7, EM3~EM7 저장하기)
def CheckCluster(data, Nearest_data, input_data, target):
  # EM
  EM_list = [];
  for k in range(3,8):
    Movies_scaled = normalize(data)
    df = pd.DataFrame(Movies_scaled)
    model = GaussianMixture(n_components=k, max_iter=20, random_state=0, covariance_type='spherical').fit(df)
    predict = model.fit_predict(df)
    # DB에 저장하기 위한 array 생성
    clu_list = [0 for i in range(k+1)]
    if(target=="MOVIE"):
      for pk in Nearest_data:
        clu_list[predict[pk-1]] += 1;
    elif(target=="USER"):
      for pk in Nearest_data:
        clu_list[predict[pk-2]] += 1;
    EM_list.append(clu_list.index(max(clu_list)))
  if(target=="MOVIE"):
    Movie_Cluster_EM(MovieId=input_data, EM3=EM_list[0], EM4=EM_list[1], EM5=EM_list[2], EM6=EM_list[3], EM7=EM_list[4]).save()
  elif(target=="USER"):
    User_Cluster_EM(UserID=input_data, EM3=EM_list[0], EM4=EM_list[1], EM5=EM_list[2], EM6=EM_list[3], EM7=EM_list[4]).save()

  # H
  H_list = [];
  for k in range(3,8):
    Movies_scaled = StandardScaler().fit_transform(data)
    df = pd.DataFrame(Movies_scaled)
    model = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward').fit(df)
    predict = model.fit_predict(df)
    # DB에 저장하기 위한 array 생성
    clu_list = [0 for i in range(k+1)]
    if(target=="MOVIE"):
      for pk in Nearest_data:
        clu_list[predict[pk-1]] += 1;
    elif(target=="USER"):
      for pk in Nearest_data:
        clu_list[predict[pk-2]] += 1;
    H_list.append(clu_list.index(max(clu_list)))
  if(target=="MOVIE"):
    Movie_Cluster_Hmeans(MovieId=input_data, H3=H_list[0], H4=H_list[1], H5=H_list[2], H6=H_list[3], H7=H_list[4]).save()
  elif(target=="USER"):
    User_Cluster_Hmeans(UserID=input_data, H3=H_list[0], H4=H_list[1], H5=H_list[2], H6=H_list[3], H7=H_list[4]).save()

  # KM
  K_list = [];
  for k in range(3,8):
    df = pd.DataFrame(data)
    model = KMeans(n_clusters=k, algorithm='auto').fit(df)
    predict = model.labels_
    # DB에 저장하기 위한 array 생성
    clu_list = [0 for i in range(k+1)]
    if(target=="MOVIE"):
      for pk in Nearest_data:
        clu_list[predict[pk-1]] += 1;
    elif(target=="USER"):
      for pk in Nearest_data:
        clu_list[predict[pk-2]] += 1;
    K_list.append(clu_list.index(max(clu_list)))
  if(target=="MOVIE"):
    Movie_Cluster_Kmeans(MovieId=input_data, K3=K_list[0]+1, K4=K_list[1]+1, K5=K_list[2]+1, K6=K_list[3]+1, K7=K_list[4]+1).save()
  elif(target=="USER"):
    User_Cluster_Kmeans(UserID=input_data, K3=K_list[0]+1, K4=K_list[1]+1, K5=K_list[2]+1, K6=K_list[3]+1, K7=K_list[4]+1).save()


# # # # # # # # # # # # # # # # ## # # # # # User KNN # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def create_User():
  Users = pd.read_csv('./api/fixtures/user_rating.csv', header=0)
  users_pk = Users['user_pk']
  Users = Users[label]
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

@api_view(["GET", "POST"])
def KNN_algorithm_user(request):
  Users, users_pk = create_User()
  input_user_score = []
  for N in request.data.get('scores'):
    input_user_score.append(float(N))
  input_user_pk = request.data.get('pk')
  input_user = Profile.objects.get(pk=input_user_pk)
  add_user_rating(input_user_score, input_user_pk)

  users_distance = []; # 유저간의 거리 리스트
  input_user_score = np.array(input_user_score)
  for user_score, user_pk in zip(Users.values, users_pk):
    dis = distance_user(input_user_score, user_score)
    users_distance.append(dis)

  Nearest_user = [] # 가장 가까운 유저 리스트 7개
  for i in range(7):
    idx = find_near_user(users_distance)
    Nearest_user.append(idx+2)
    users_distance[idx] = 100
  print(Nearest_user)
  target = "USER"
  CheckCluster(Users, Nearest_user, input_user, target)
  return Response(status=status.HTTP_200_OK)

# 신규유저가 평점을 남긴 적이 있는지 확인
@api_view(['GET', 'POST'])
def checkCSV(request):
  pk = request.data.get('pk')
  flag = False
  Users = pd.read_csv('./api/fixtures/user_rating.csv', header=0)
  Users = Users['user_pk']
  for user_pk in Users:
    if(user_pk==pk):
      flag = True; break;
  return Response(data=flag, status=status.HTTP_200_OK)
