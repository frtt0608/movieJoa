from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, Rate, Profile, Cluster, Subscription_manager, Matrix
from api.serializers import SubscriptionSerializer, MovieSerializer

from django.core import serializers
from rest_framework.response import Response
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import normalize, StandardScaler
import random
from django.db.models import Avg
from sklearn.cluster import AgglomerativeClustering

@api_view(['GET', 'POST', 'DELETE'])
def make(request):
    ### 이건 쓰지 않을 것입니다. gogo(request) 로 변경 예정.
    ## 1. 변수 정의
    # 1-1. array : array 에 있는 데이터를 csv로 변환할 것입니다.
    # 예시 array[0] = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Toy Story (1995)']
    # toy story라는 영화는 0011100000000000이라는 장르데이터를 가진다는 것을 의미합니다.

    # 하나의 영화가 어떠한 장르를 포함하는지 0, 1로 표시할 것이며 행에는 하나의 영화 데이터를 넣을 것입니다.
    # 열에는 장르 이름을 의미합니다.
    array = []

    # 1-2. genre_number: array에 들어가는 장르의 인덱스입니다. ( 열 ) / 총 19개(18+영화이름넣을공간1) 입니다.
    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
                    'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
                    'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}

    ## 2. array 만들기
    # 2-1. 전체 영화를 가져오고, 총 몇개의 영화인지 확인합니다.
    movies = Movie.objects.all()
    # last_movie_id = movies[len(movies)-1].id
    movies_count = len(movies)
    '''
    id,Action,Adventure,Animation,Children's,Comedy,Crime,Documentary,Drama,Fantasy,Film-Noir,Horror,Musical,Mystery,Romance,Sci-Fi,Thriller,War,Western
    '''
    # 2-2. 하나의 영화데이터를 tmp_array 에 담아서 array로 보내기.
    for i in range(movies_count):
        # print(movies[i], '이게 정보이다.')
        tmp_array = [0]*19
        tmp_array[0]=movies[i].id
        # tmp_array[1]=movies[i].title
        movie_genres = movies[i].genres.split('|')

        for j in range(len(movie_genres)):
            # print(movie_genres[j], end=' ')
            # print(genre_number[movie_genres[j]]+2, end=' ')
            tmp_array[genre_number[movie_genres[j]]+1] = 1

        array.append(tmp_array)

    # 2-3. csv 파일로 array 를 저장하자.
    df = pd.DataFrame(array)
    df.to_csv("test.csv", header=None, index=None)

    return Response(status=status.HTTP_200_OK)

# @api_view(['GET', 'POST'])
# def gogo(request):
#     ## 1. 변수 정의
#     # 1-1. array : array 에 있는 데이터를 csv로 변환할 것입니다.
#     # 예시 array[0] = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Toy Story (1995)']
#     # toy story라는 영화는 0011100000000000이라는 장르데이터를 가진다는 것을 의미합니다.
#
#     # 하나의 영화가 어떠한 장르를 포함하는지 0, 1로 표시할 것이며 행에는 하나의 영화 데이터를 넣을 것입니다.
#     # 열에는 장르 이름을 의미합니다.
#     array = []
#
#     # 1-2. genre_number: array에 들어가는 장르의 인덱스입니다. ( 열 ) / 총 19개(18+영화이름넣을공간1) 입니다.
#     genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
#                     'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
#                     'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}
#
#     ## 2. array 만들기
#     # 2-1. 전체 영화를 가져오고, 총 몇개의 영화인지 확인합니다.
#     movies = Movie.objects.all()
#     # last_movie_id = movies[len(movies)-1].id
#     movies_count = len(movies)
#     '''
#     id,Action,Adventure,Animation,Children's,Comedy,Crime,Documentary,Drama,Fantasy,Film-Noir,Horror,Musical,Mystery,Romance,Sci-Fi,Thriller,War,Western
#     '''
#     # 2-2. 하나의 영화데이터를 tmp_array 에 담아서 array로 보내기.
#     for i in range(movies_count):
#         # print(movies[i], '이게 정보이다.')
#         tmp_array = [0]*19
#         tmp_array[0]=movies[i].id
#         # tmp_array[1]=movies[i].title
#         movie_genres = movies[i].genres.split('|')
#
#         for j in range(len(movie_genres)):
#             # print(movie_genres[j], end=' ')
#             # print(genre_number[movie_genres[j]]+2, end=' ')
#             tmp_array[genre_number[movie_genres[j]]+1] = 1
#
#         array.append(tmp_array)
#
#
#     # 2-3. csv 파일로 array 를 저장하자.
#     # df = pd.DataFrame(array)
#     # print(df)
#     # print()
#     # df_slice = df.loc[:,1:]
#     # print(df_slice)
#
#     # # 여기 profile pk 를 변수로 설정해야한다!!!!!!!!!!!!!
#     profile = Profile.objects.get(pk=2)
#     rates = Rate.objects.filter(UserID=profile.user.id).order_by('-rating')[:5]
#     #
#     # # 평점을 잘 준 댓글들의 영화 장르들을 파악합니다.
#     box = [0]*19
#     box[0] = profile.id
#     genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,
#                        'Crime':5,'Documentary':6,'Drama':7,'Fantasy':8,'Film-Noir':9,
#                        'Horror':10, 'Musical':11, 'Mystery':12,'Romance':13,'Sci-Fi':14,
#                        'Thriller':15,'War':16,'Western':17}
#     for rate in rates:
#         genres = rate.MovieID.genres.strip().split('|')
#         # print(genres)
#         for genre in genres:
#             box[genre_number[genre]+1] += 1/len(rates)
#
#     array.append(box)
#     df = pd.DataFrame(array)
#     data_slice = df.loc[:, 1:]
#
#     cluster = Cluster.objects.get(pk=1)
#     cluster_n = cluster.n_component
#     cluster_way = cluster.way
#
#     # 3. 클러스터링 합니다.
#     if cluster_way == 'H':
#         data_scaled = StandardScaler().fit_transform(data_slice)
#         df_end = pd.DataFrame(data_scaled)
#         model = AgglomerativeClustering(n_clusters=cluster_n, affinity='euclidean', linkage='ward').fit(df_end)
#         y_predict = model.fit_predict(df_end)
#
#     elif cluster_way == 'MF':
#         matrix = Matrix.objects.filter(UserID=profile)[0]
#
#         movies_id = []
#
#         movies_id.append(matrix.Movie1.id)
#         movies_id.append(matrix.Movie2.id)
#         movies_id.append(matrix.Movie3.id)
#         movies_id.append(matrix.Movie4.id)
#         movies_id.append(matrix.Movie5.id)
#         movies_id.append(matrix.Movie6.id)
#         movies_id.append(matrix.Movie7.id)
#         movies_id.append(matrix.Movie8.id)
#         movies_id.append(matrix.Movie9.id)
#         movies_id.append(matrix.Movie10.id)
#
#         movies = Movie.objects.filter(id__in=movies_id)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     else:
#         # EM을 기준으로 합시다 > KNN, EM, K 일때 여기로 들어옴.
#         data_scaled = StandardScaler().fit_transform(data_slice)
#         df_end = pd.DataFrame(data_scaled)
#         model = GaussianMixture(n_components=cluster_n, max_iter=20, random_state=0, covariance_type='spherical').fit(df_end)
#         y_predict = model.fit_predict(df_end)
#
#     # print(y_predict)
#     # 4. 나의 넘버(y_predict[-1]를 통해 클러스터링 영화들을 가져옵니다.)
#     cluster_number = y_predict[-1]
#     # print(cluster_number)
#     cluster_movies = [int(df[x:x+1].values[0][0]) for x in range(len(y_predict)-1) if y_predict[x]==y_predict[-1]]
#
#     # cluster_movies = [data_slice[x:x+1].values[0][1] for x in range(len(y_predict)-1) if y_predict[x]==y_predict[-1]]
#     # print(cluster_movies)
#     pick_movies = random.sample(cluster_movies, k=10)
#     movies = Movie.objects.filter(id__in=pick_movies).order_by('-watch_count')
#     serializer = MovieSerializer(movies, many=True)
#
#     return Response(data=serializer.data, status=status.HTTP_200_OK)
#
