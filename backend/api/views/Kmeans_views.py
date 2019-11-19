from api.models import Movie_Cluster_Kmeans, User_Cluster_Kmeans, Movie, Profile, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sklearn.cluster import KMeans
import csv
import random

# @api_view(['GET'])
# def kmeans_movie(request, k, genres):
#   genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,
#                   'Crime':5,'Documentary':6,'Drama':7,'Fantasy':8,'Film-Noir':9, 
#                   'Horror':10, 'Musical':11, 'Mystery':12,'Romance':13,'Sci-Fi':14,
#                   'Thriller':15,'War':16,'Western':17}
#   my_list = []
#   genre_cnt = [[0 for i in range(18)] for j in range(k+1)]
  

#   if request.method == 'GET':
#     movies = Movie_Cluster_Kmeans.objects.all();
#     Kcluster_movie = [[] for j in range(k+1)]
#     if k==3:
#       for movie in movies:
#         index = movie["K3"]
#         Kcluster_movie[index].append(movie["MovieId"])
#     elif k==4:
#       for movie in movies:
#         index = movie["K4"]
#         Kcluster_movie[index].append(movie["MovieId"])
#     elif k==5:
#       for movie in movies:
#         index = movie["K5"]
#         Kcluster_movie[index].append(movie["MovieId"])
#     elif k==6:
#       for movie in movies:
#         index = movie["K6"]
#         Kcluster_movie[index].append(movie["MovieId"])
#     else:
#       for movie in movies:
#         index = movie["K7"]
#         Kcluster_movie[index].append(movie["MovieId"])
    
#     # 선택한 장르를 인덱스로 표시
#     for genre in genres:
#       my_list.append(genre_number[genre])

#     # 각 군집에 속해있는 영화의 장르 카운트
#     for i in range(1,k+1):
#       for movie_pk in Kcluster_movie[i]:
#         movie = Movie.objects.get(pk=movie_pk)
#         genres = movie.genres
#         for genre in genres:
#           genre_i = genre_number[genre]
#           genre_cnt[i][genre_i] += 1
    
#     # 군집마다 가중치 부여, 가장 유사한 영화찾기
#     all_Score = [0 for i in range(k+1)]
#     for i in range(len(my_list)):
#       L = my_list(i)
#       score = 0
#       if(i==0):
#         for j in range(1,k+1):
#           all_Score[j] += genre_cnt[j][L] * 10
#       elif(i==1):
#         for j in range(1,k+1):
#           all_Score[j] += genre_cnt[j][L] * 5
#       else:
#         for j in range(1, k+1):
#           all_Score[j] += genre_cnt[j][L]
#     print(all_Score)

#     # 가장 유사한 영화 군집 저장
#     my_cluster = Kcluster_movie[all_Score.index(max(all_Score))]
#     my_movie = random.sample(my_cluster, 5)

#     return Response(data=my_movie, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def kmeans_user(request, user_pk, k):
#   genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,
#                   'Crime':5,'Documentary':6,'Drama':7,'Fantasy':8,'Film-Noir':9, 
#                   'Horror':10, 'Musical':11, 'Mystery':12,'Romance':13,'Sci-Fi':14,
#                   'Thriller':15,'War':16,'Western':17}
#   my_list = []
#   genre_cnt = [[0 for i in range(18)] for j in range(k+1)]
  
#   if request.method == 'GET':
#     users = User_Cluster_Kmeans.objects.all();
#     Kcluster_user = [[] for j in range(k+1)]
#     if k==3:
#       for user in users:
#         index = user["K3"]
#         Kcluster_user[index].append(user["UserID"])
#     elif k==4:
#       for user in users:
#         index = user["K4"]
#         Kcluster_user[index].append(user["UserID"])
#     elif k==5:
#       for user in users:
#         index = user["K5"]
#         Kcluster_user[index].append(user["UserID"])
#     elif k==6:
#       for user in users:
#         index = user["K6"]
#         Kcluster_user[index].append(user["UserID"])
#     else:
#       for user in users:
#         index = user["K7"]
#         Kcluster_user[index].append(user["UserID"])

# way = KM, K = 3, movie_pk = 427
# cluster_num = Movie_Cluster_Kmeans.objects.get(MovieId = movie_pk)["K3"]
# clusters = Movie_Cluster_Kmeans.objects.filter(K3=cluster_num)

# way = KM, K = 3, user_pk = 36
# cluster_num = User_Cluster_Kmeanse.objects.get(UserID = user_pk)["K3"]
# cluster = User_Cluster_Kmeans.objects.filter(K3=cluster_num)

@api_view(['GET', 'POST'])
def create_movie_clu(request):
  if request.method == 'GET':
    f = open('api/fixtures/K_movie.csv', 'r', encoding='utf-8', newline='')
    wr = csv.reader(f)
    for line in wr:
      movie_pk = int(line[0])
      movie = Movie.objects.get(pk=movie_pk);
      Movie_Cluster_Kmeans(
        MovieId = movie,
        K3 = int(line[1]),
        K4 = int(line[2]),
        K5 = int(line[3]),
        K6 = int(line[4]),
        K7 = int(line[5])).save()

@api_view(['GET', 'POST'])
def create_user_clu(request):
  if request.method == 'GET':
    f = open('api/fixtures/K_user.csv', 'r', encoding='utf-8', newline='')
    wr = csv.reader(f)
    for line in wr:
      if line[0]!='user_pk':
        number = str(int(line[0])+1)
        user = User.objects.get(pk=number)
        profile = Profile.objects.get(user=user)
        User_Cluster_Kmeans(
        UserID = profile,
        K3 = int(line[1]),
        K4 = int(line[2]),
        K5 = int(line[3]),
        K6 = int(line[4]),
        K7 = int(line[5])).save()
        # print(wr)


# # * * * * * * * * * * * * * * 유저 메인문  * * * * * * * * * * * * * * * *

# group = pd.read_csv("./api/fixtures/user_clu.csv", header=0)
# group = group[["Action","Adventure","Animation","Children's",
#                 "Comedy","Crime","Documentary","Drama","Fantasy",
#                 "Film-Noir","Horror","Musical","Mystery","Romance",
#                 "Sci-Fi","Thriller","War","Western"]]

# group.head()
# model1 = kmeans(3, group)
# users_Kmeans = model1.train_cluster()[1]

# cluster_1 = [];
# cluster_2 = [];
# cluster_3 = [];

# for i in range(len(users_Kmeans)):
#   if users_Kmeans[i]==1:
#     cluster_1.append(i+1)
#   elif users_Kmeans[i]==2:
#     cluster_2.append(i+1)
#   else:
#     cluster_3.append(i+1)

# my_pk = 62
# my_cluster = []

# my_genre = group.values[my_pk-1]

# if my_pk in cluster_1:
#   my_cluster = cluster_1
# elif my_pk in cluster_2:
#   my_cluster = cluster_2
# elif my_pk in cluster_3:
#   my_cluster = cluster_3

# genre_rate = my_genre[::]
# genres_index = []

# for cnt in range(3):
#   max_rate = 0
#   idx = 0
#   for i in range(len(genre_rate)):
#     if max_rate < genre_rate[i]:
#       max_rate = genre_rate[i]
#       idx = i
#   genre_rate[idx] = 0
#   genres_index.append(idx)

# clu_users = []

# for user_id in my_cluster:
#   clu_user = group.values[user_id-1]
#   temp = 0.0;
#   for genre_index in genres_index:
#     temp += ((my_genre[genre_index] - clu_user[genre_index])**2)**0.5
#   temp = round(temp, 2)
#   clu_users.append(temp)


# my_users = []

# for cnt in range(5):
#   min_user = 999
#   idx = 0
#   for i in range(len(clu_users)):
#     if min_user > clu_users[i]:
#       min_user = clu_users[i]
#       idx = i
#   clu_users[idx] = 999
#   my_users.append(idx)

# print("< - < < - < - < - my user - > - > - > - > - >")
# print(my_users)
