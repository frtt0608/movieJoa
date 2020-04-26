from rest_framework.decorators import api_view
from api.models import User_Cluster_EM, Movie_Cluster_EM, Profile, Movie
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

@api_view(['POST'])
def user_emcluster(request):
    users = request.data.get('clustering', None)
    
    for user in users:
        id = user.get('user_pk')
        EM3 = user.get('EM3')
        EM4 = user.get('EM4')
        EM5 = user.get('EM5')
        EM6 = user.get('EM6')
        EM7 = user.get('EM7')
        User_Cluster_EM(UserID=Profile.objects.get(user=User.objects.get(pk=id)), EM3=EM3, EM4=EM4, EM5=EM5, EM6=EM6, EM7=EM7).save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def movie_emcluster(request):
    movies = request.data.get('clustering', None)
    
    for movie in movies:
        title = movie.get('title')
        EM3 = movie.get('EM3')
        EM4 = movie.get('EM4')
        EM5 = movie.get('EM5')
        EM6 = movie.get('EM6')
        EM7 = movie.get('EM7')
        Movie_Cluster_EM(MovieId=Movie.objects.get(title=title), EM3=EM3, EM4=EM4, EM5=EM5, EM6=EM6, EM7=EM7).save()
    return Response(status=status.HTTP_200_OK)