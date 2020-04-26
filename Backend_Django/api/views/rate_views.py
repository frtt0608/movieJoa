from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Profile, Rate
from api.serializers import MovieSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
import pprint

@api_view(['GET', 'POST', 'DELETE'])
def ratings(request):
 	# if request.method == 'GET':
    #     id = request.GET.get('id', request.GET.get('movie_id', None))
    #     title = request.GET.get('title', None)
	#
    #     movies = Movie.objects.all()
	#
    #     if id:
    #         movies = movies.filter(pk=id)
    #     if title:
    #         movies = movies.filter(title__icontains=title)
	#
    #     serializer = MovieSerializer(movies, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

	if request.method == 'POST':
		rating_data = request.data.get('ratings', None)
		for rating in rating_data:

			UserID = rating.get('UserID', None)
			MovieID = rating.get('MovieID', None)
			Rating = rating.get('Rating', None)
			Timestamp = rating.get('Timestamp', None)
			
			Rate(UserID=Profile.objects.get(pk=UserID),
				MovieID=Movie.objects.get(pk=int(MovieID)),
				rating=Rating, Timestamp=Timestamp).save()

		return Response(status=status.HTTP_200_OK)

# @api_view(['POST'])
# def checkRating(request, movie_pk):
#   pprint.pprint(request.data)
#   if request.method == 'POST':
#     rates = Rate.objects.filter(MovieID=movie_pk) # 영화에 담긴 평점 모두 가져오기
#     user_pk = request.data.get('user_pk')         # 유저
#     profile = Profile.objects.get(user=user_pk)   # 유저의 프로필
#     rate = rates.objects.get(UserID=profile.pk, default=None)        # 유저가 영화에 남긴 평점 가져오기
#     print(rate)
#     if(rate==[]):
#       return Response(data=False, status=status.HTTP_200_OK)
#     else:
#       return Response(data=True, status=status.HTTP_200_OK)

@api_view(['PUT', 'POST', 'DELETE'])
def cduRating(request, movie_pk):
  pprint.pprint(request.data)
  rates = Rate.objects.filter(MovieID=movie_pk) # 영화에 담긴 평점 모두 가져오기
  user_pk = request.data.get("user_pk", None)   # 유저
  profile = Profile.objects.get(user=user_pk)   # 유저의 프로필
  flag = False
  for rate in rates:
    if rate.UserID == profile:
      flag = True
      break
  # 평점 등록 POST
  if request.method == "POST":
    if(flag==True):
      return Response(data=False, status=status.HTTP_200_OK)
    else:
      score = request.data.get("score")
      Rate(UserID=profile,
				MovieID=Movie.objects.get(pk=movie_pk),
				rating=score, Timestamp=0).save()
      return Response(data=True, status=status.HTTP_200_OK)
  # 평점 삭제 DELETE
  elif request.method == "DELETE":
    if(flag==False): 
      return Response(data=False, status=status.HTTP_200_OK)
    else:
      rate.delete()
      return Response(data=True, status=status.HTTP_200_OK)
  # 평점 수정 PUT
  elif request.method == "PUT":
    if(flag==False):
      return Response(data=False, status=status.HTTP_200_OK)
    else:
      score = request.data.get("score")
      rate.rating = score
      rate.save()
      return Response(data=True, status=status.HTTP_200_OK)
