from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rate, Cluster, Profile
from api.serializers import MovieSerializer, Movie_Age_Serializer
from rest_framework.response import Response
from django.db.models import Avg
import pandas as pd
import random

from imdb import IMDb

@api_view(['GET', 'POST', 'DELETE'])
def getmovies(request):

    # create an instance of the IMDb class
    ia = IMDb()

    # setting movies
    movies = Movie.objects.all()

    # nogetmovie = [] # search_movie 불가능 목록
    # notitle = [] 
    # nocasting = []
    # nourl = []
    # nodirector = []
    # noplot = []
    # cnt = 0
    for mov in movies:
        name = mov.title
        # 뭐든 없는게 있을거다 믿지마라 그러므로 value는 get으로 꺼내자
        getmovie = ia.search_movie(name)
        if getmovie:
            movieid = getmovie[0].movieID
            movie = ia.get_movie(movieid)
            
            title = movie.data.get('original title')
            # if not title:
            #     notitle.append([cnt, name])
            # print('title : {}'.format(title))

            castings = movie.data.get('cast')
            if castings:
                casting = []
                for i in castings:
                    casting.append(i['name'])
                casting = '|'.join(casting)
                mov.casting = casting
            # else:
            #     nocasting.append([cnt, name])
            # print('castings : {}'.format(casting))

            url = movie.data.get('cover url')
            if url:
                url = url[:url.index('._V1')] + '._V1_SY1000_SX670_AL_.jpg'
                mov.url = url
                # print(cnt,' : ',url)
            # else:
            #     nourl.append([cnt, name])
            # print('cover url : {}'.format(url))
            # @._V1_SX101_CR0,0,101,150_.jpg -> @._V1_SY1000_SX670_AL_.jpg

            director = movie.data.get('directors')
            if director:
              director = director[0]
              mov.director = director
            # print('director : {}'.format(director))
            # else:
            #     nodirector.append([cnt, name])
            # # print(movie.data) # data.get('plot')

            plot = movie.data.get('plot')
            if plot:
                plot = plot[0]
                if '::' in plot:
                    plot = plot[:plot.index('::')]
                mov.plot = plot
            # else:
            #     noplot.append([cnt, name])
            # print('plot : {}'.format(plot))

        # else:
        #     nogetmovie.append([cnt, name])
            # print(name, '999999999999i')
        mov.save()

    # print('------------------------------nogetmovie')
    # print(nogetmovie) # search_movie 불가능 목록
    # print('------------------------------notitle')
    # print(notitle)
    # print('------------------------------nocasting')
    # print(nocasting)
    # print('------------------------------nourl')
    # print(nourl)
    # print('------------------------------nodirector')
    # print(nodirector)
    # print('------------------------------noplot')
    # print(noplot)
    # print()
    print('끝')
    return Response(status=status.HTTP_200_OK)
