from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rate, Profile
from django.contrib.auth.models import User
from api.serializers import MovieSerializer, ProfileSerializer
from rest_framework.response import Response

# 영화 수정 movie_udpate
@api_view(['POST', 'PUT'])
def movie_update(request, movie_pk):
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=movie_pk)
        movie.title = request.data.get('title')
        genres = request.data.get('genres_array')
        movie.genres = '|'.join(genres)
        movie.save()
    return Response(status=status.HTTP_200_OK)

# 영화 삭제 movie_delete
@api_view(['POST', 'DELETE'])
def movie_delete(request, movie_pk):
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=movie_pk)
        movie.delete()
    return Response(status=status.HTTP_200_OK)

#  유저 수정 user_update
@api_view(['POST', 'PUT'])
def profile_update(request, user_pk):
    if request.method == 'PUT':
        profile = Profile.objects.get(pk = user_pk)
        profile.gender = request.data.get('gender')
        profile.age = request.data.get('age')
        profile.occupation = request.data.get('occupation')
        profile.user.username = request.data.get('username')
        profile.save()
    return Response(status=status.HTTP_200_OK)

# 유저 삭제 user_delete
@api_view(['POST', 'DELETE'])
def profile_delete(request, user_pk):
    if request.method == 'DELETE':
        user = User.objects.get(pk=user_pk)
        user.delete()
    return Response(status=status.HTTP_200_OK)