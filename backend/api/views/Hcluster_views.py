from rest_framework.decorators import api_view
from api.models import User_Cluster_Hmeans, Movie_Cluster_Hmeans, Profile, Movie
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

@api_view(['POST'])
def user_hcluster(request):
    users = request.data.get('clustering', None)

    for user in users:
        id = user.get('user_pk')
        H3 = user.get('H3')
        H4 = user.get('H4')
        H5 = user.get('H5')
        H6 = user.get('H6')
        H7 = user.get('H7')
        # cluster data를 받아 객체 생성 및 추가
        User_Cluster_Hmeans(UserID=Profile.objects.get(user=User.objects.get(pk=id)), H3=H3, H4=H4, H5=H5, H6=H6, H7=H7).save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def movie_hcluster(request):
    movies = request.data.get('clustering', None)

    for movie in movies:
        title = movie.get('title')
        H3 = movie.get('H3')
        H4 = movie.get('H4')
        H5 = movie.get('H5')
        H6 = movie.get('H6')
        H7 = movie.get('H7')
        # cluster data를 받아 객체 생성 및 추가
        Movie_Cluster_Hmeans(MovieId=Movie.objects.get(title=title), H3=H3, H4=H4, H5=H5, H6=H6, H7=H7).save()
    return Response(status=status.HTTP_200_OK)