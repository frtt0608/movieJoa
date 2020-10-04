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

    for mov in movies:
        name = mov.title
    
        getmovie = ia.search_movie(name)
        if getmovie:
            movieid = getmovie[0].movieID
            movie = ia.get_movie(movieid)
            
            title = movie.data.get('original title')

            castings = movie.data.get('cast')
            if castings:
                casting = []
                for i in castings:
                    casting.append(i['name'])
                casting = '|'.join(casting)
                mov.casting = casting

            url = movie.data.get('cover url')
            if url:
                url = url[:url.index('._V1')] + '._V1_SY1000_SX670_AL_.jpg'
                mov.url = url

            director = movie.data.get('directors')
            if director:
              director = director[0]
              mov.director = director

            plot = movie.data.get('plot')
            if plot:
                plot = plot[0]
                if '::' in plot:
                    plot = plot[:plot.index('::')]
                mov.plot = plot

        mov.save()

    return Response(status=status.HTTP_200_OK)
