from api.models import Movie_Cluster_Kmeans, User_Cluster_Kmeans, Movie, Profile, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sklearn.cluster import KMeans
import csv
import random

@api_view(['GET', 'POST'])
def create_movie_clu(request):
  if request.method == 'GET':
    f = open('api/fixtures/K_movie.csv', 'r', encoding='utf-8', newline='')
    wr = csv.reader(f)
    for line in wr:
      movie_pk = int(line[0])
      movie = Movie.objects.get(pk=movie_pk)
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