from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from api.models import Profile, Subscription_manager, Rate, Cluster, Movie, Matrix
from rest_framework.response import Response
from api.serializers import SubscriptionSerializer, MovieSerializer
import datetime
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import normalize, StandardScaler
import random
from django.db.models import Avg
from sklearn.cluster import AgglomerativeClustering


@api_view(['POST'])
def create(request):
    if request.method == 'POST':

    # Subscription_manager 이라는 모델에 생성을 해야 한다.
        username = request.data.get('user')
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        check_subscription_request = Subscription_manager.objects.filter(Profile=profile, approval=False)
        if check_subscription_request:
            message = {'create':False, 'message':'이미 구독 신청을 한 상태입니다.'}
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            message = {'create':True, 'message':'구독 신청이 되었습니다.'}
            subscription_request = Subscription_manager.objects.create(
                Profile=profile,
                request=request.data.get('request'),
                approval=False,
            )
            return Response(data=message, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def manager(request):
    if request.method == 'GET':
        subscriptions = Subscription_manager.objects.filter(approval=False)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        subscription = request.data.get('subscription')
        profile = Profile.objects.get(pk=subscription['Profile'])

        # 1. Profile 변경 (처음 신청했을 때, 만료 이후 재신청했을 때, 연장신청했을 때 모두 여기에 해당한다.)

        if profile.subscription.strftime("%Y%m%d") > datetime.datetime.now().strftime("%Y%m%d"):
            # 이것이 바로 연장
            profile.subscription = profile.subscription + datetime.timedelta(days=subscription['request'])
            profile.save()
        else:
            # 이것은 처음 신청, 또는 만료 이후 다시 신청
            profile.approval = True
            profile.subscription = datetime.datetime.now() + datetime.timedelta(days=subscription['request'])
            profile.save()

        # 2. Subscription_manager 에서 해당 객체 승인 되었다고 변경
        subscription_instance = Subscription_manager.objects.get(pk=subscription['id'])
        subscription_instance.approval = True
        subscription_instance.save()

        return Response(status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def itembased_movies(request, profile_pk):
    # csv 파일을 토대로 하는 것이므로, 새로운 회원에게 적용되어선 안됩니다. 그래서 이 함수는 사실상 쓰이지 않고
    # 아래에 있는 itembased_movies2 함수가 쓰일 것입니다.

    # 이 함수는 구독서비스를 이용하는 사용자에게 itembased 추천을 하는 함수입니다.
    # 과정은 아래와 같습니다.
    # 0. 나의 선호 영화 장르 파악하기(box)
    # 1. csv 가져오기
    # 2. 1에 box 추가하고
    # 3. 저장된 방식의 클러스터링 알고리즘 적용(K-means, H, EM, KNN, MF 인지 확인)한 이후 적합한 방법으로 ㄱ
    # 4. 마지막 클러스터링 넘버랑 같은 넘버 영화를 가져온다

    # 0. 내가 어떠한 것을 좋아하는지 평점을 통해 알아냅니다.
    profile = Profile.objects.get(pk=profile_pk)
    rates = Rate.objects.filter(UserID=profile.user.id).order_by('-rating')[:5]

    # 평점을 잘 준 댓글들의 영화 장르들을 파악합니다.
    box = [0]*18
    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,
                       'Crime':5,'Documentary':6,'Drama':7,'Fantasy':8,'Film-Noir':9,
                       'Horror':10, 'Musical':11, 'Mystery':12,'Romance':13,'Sci-Fi':14,
                       'Thriller':15,'War':16,'Western':17}
    for rate in rates:
        genres = rate.MovieID.genres.strip().split('|')
        # print(genres)
        for genre in genres:
            box[genre_number[genre]] += 1/len(rates)
    # box : User 의 영화 장르 평점입니다! 이걸 이용해서 클러스링 돌리고 친구들 가져옵시다!

    # 1. data를 가져올 때 파일을 가져오는데 기본 위치는 backend입니다.
    # data = pd.read_csv("../data/movie_clu.csv")
    data = pd.read_csv("./api/fixtures/movie_clu.csv")
    data_slice = data[['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]

    # 2. 나의 성향(box)을 1에 추가합니다.
    # print(data_slice[-1:][:])
    data_slice.loc[3883,:] = box
    # print(data_slice[-1:][:])

    cluster = Cluster.objects.get(pk=1)
    cluster_n = cluster.n_component
    cluster_way = cluster.way

    # 3. 클러스터링 합니다.
    if cluster_way == 'H':
        data_scaled = StandardScaler().fit_transform(data_slice)
        df = pd.DataFrame(data_scaled)
        model = AgglomerativeClustering(n_clusters=cluster_n, affinity='euclidean', linkage='ward').fit(df)
        y_predict = model.fit_predict(df)

    elif cluster_way == 'MF':
        matrix = Matrix.objects.filter(UserID=profile)[0]

        movies_id = []

        movies_id.append(matrix.Movie1.id)
        movies_id.append(matrix.Movie2.id)
        movies_id.append(matrix.Movie3.id)
        movies_id.append(matrix.Movie4.id)
        movies_id.append(matrix.Movie5.id)
        movies_id.append(matrix.Movie6.id)
        movies_id.append(matrix.Movie7.id)
        movies_id.append(matrix.Movie8.id)
        movies_id.append(matrix.Movie9.id)
        movies_id.append(matrix.Movie10.id)

        movies = Movie.objects.filter(id__in=movies_id)
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    else:
        # EM을 기준으로 합시다 > KNN, EM, K 일때 여기로 들어옴.
        data_scaled = StandardScaler().fit_transform(data_slice)
        df = pd.DataFrame(data_scaled)
        model = GaussianMixture(n_components=cluster_n, max_iter=20, random_state=0, covariance_type='spherical').fit(df)
        y_predict = model.fit_predict(df)

    # 4. 나의 넘버(y_predict[-1]를 통해 클러스터링 영화들을 가져옵니다.)
    cluster_number = y_predict[-1]
    cluster_movies = [data[x:x+1].values[0][-1] for x in range(len(y_predict)-1) if y_predict[x]==y_predict[-1]]
    pick_movies = random.sample(cluster_movies, k=10)
    movies = Movie.objects.filter(title__in=pick_movies).order_by('-watch_count')
    serializer = MovieSerializer(movies, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def userbased_movies(request, profile_pk):
    # 이 함수는 구독서비스를 이용하는 사용자에게 userbased 추천을 하는 함수입니다.
    # 과정은 아래와 같습니다.
    # 0. 나와 유사한 사람(이미 클러스터링을 통해 나온 값들입니다.)확인
    # 1. 그 사람들이 남긴 평점들을 가져옵니다.
    # 2. 해당 평점들을 예쁘게 나열, 정렬시킵니다.
    # 3. 일부분 영화를 추가하고, 해당 영화들을 반환합니다.
    if request.method == 'POST':
    # 0 : 나와 유사한 사람(resemble_users), 유사한 영화들을 담을 movie_box(나중에 배열로 형변환됨.)
        resemble_users = request.data.get('resemble_users')
        movie_box = {}
    # 1
        for i in range(len(resemble_users)-1):
            num = resemble_users[i]['id']
            profile = Profile.objects.get(pk=num)
            rates = profile.profile_rate.order_by('rating')[:5]
            for rate in rates:
                # movie_box = {'영화키값':[평점sum, 평점count]}
                if movie_box.get(rate.MovieID)==None:
                    movie_box.update({rate.MovieID:[rate.rating,1]})
                else:
                    tmp_array = movie_box.get(rate.MovieID)
                    tmp_array[0] += rate.rating
                    tmp_array[1] += 1
    # 2
        movie_box = sorted(movie_box.items(), key=lambda x : (x[1][0]/x[1][1], x[1][1]), reverse=True)
        movie_box = movie_box[:10]

    # 3
        movie_array = []
        for i in movie_box:
            movie_array.append(i[0])

        serializer = MovieSerializer(movie_array, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def itembased_movies2(request, profile_pk):
    # 이 함수는 구독서비스를 이용하는 사용자에게 itembased 추천을 하는 함수입니다.
    # 과정은 아래와 같습니다.

    # 1. 영화 장르 데이터를 2차 배열로 생성 (array)
    # 2. 사용자의 평점을 기반으로 좋아하는 장르 분포도 조사 (box)
    # 3. array에 box를 추가하고 clustering 실시
    # 4. box와 같은 군집에 해당하는 영화들 중에서 random 10개 추출


    ## 1.
    # array : 특정 영화 id에 어떤 장르가 있는지 0,1 로 저장할 것입니다. 즉 2차배열입니다.
    # 예시 array[0] = [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # toy story(1 id를 가지는 movie)라는 영화는 0011100000000000이라는 장르데이터를 가진다는 것을 의미합니다.

    array = []

    # 1-2. genre_number: array에 들어가는 장르의 인덱스입니다. ( 열 ) / 총 19개(18+영화이름넣을공간1) 입니다.
    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,'Crime':5,'Documentary':6,
                    'Drama':7,'Fantasy':8,'Film-Noir':9, 'Horror':10, 'Musical':11, 'Mystery':12,
                    'Romance':13,'Sci-Fi':14,'Thriller':15,'War':16,'Western':17}

    movies = Movie.objects.all()
    # last_movie_id = movies[len(movies)-1].id
    movies_count = len(movies)
    '''
    id,Action,Adventure,Animation,Children's,Comedy,Crime,Documentary,Drama,Fantasy,Film-Noir,Horror,Musical,Mystery,Romance,Sci-Fi,Thriller,War,Western
    '''
    # 하나의 영화데이터를 tmp_array 에 담아서 array로 보내기.
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

    ## 2.
    # 여기 profile pk 를 변수로 설정해야한다!!!!!!!!!!!!!
    profile = Profile.objects.get(pk=profile_pk)
    rates = Rate.objects.filter(UserID=profile.user.id).order_by('-rating')[:5]

    # 그런데 내가 남긴 평점이 없다면 애초에 itembase 를 못하잖아!
    if len(rates)==0:
        return Response(data=[], status=status.HTTP_200_OK)



    # # 평점을 잘 준 댓글들의 영화 장르들을 파악합니다.
    box = [0]*19
    box[0] = profile.id
    genre_number = {'Action':0,'Adventure':1,'Animation':2,"Children's":3,'Comedy':4,
                       'Crime':5,'Documentary':6,'Drama':7,'Fantasy':8,'Film-Noir':9,
                       'Horror':10, 'Musical':11, 'Mystery':12,'Romance':13,'Sci-Fi':14,
                       'Thriller':15,'War':16,'Western':17}
    for rate in rates:
        genres = rate.MovieID.genres.strip().split('|')
        # print(genres)
        for genre in genres:
            box[genre_number[genre]+1] += 1/len(rates)

    array.append(box)
    df = pd.DataFrame(array)

    ## 3.
    data_slice = df.loc[:, 1:]

    cluster = Cluster.objects.get(pk=1)
    cluster_n = cluster.n_component
    cluster_way = cluster.way

    if cluster_way == 'H':
        data_scaled = StandardScaler().fit_transform(data_slice)
        df_end = pd.DataFrame(data_scaled)
        model = AgglomerativeClustering(n_clusters=cluster_n, affinity='euclidean', linkage='ward').fit(df_end)
        y_predict = model.fit_predict(df_end)

    elif cluster_way == 'MF':
        matrix = Matrix.objects.filter(UserID=profile)[0]

        movies_id = []

        movies_id.append(matrix.Movie1.id)
        movies_id.append(matrix.Movie2.id)
        movies_id.append(matrix.Movie3.id)
        movies_id.append(matrix.Movie4.id)
        movies_id.append(matrix.Movie5.id)
        movies_id.append(matrix.Movie6.id)
        movies_id.append(matrix.Movie7.id)
        movies_id.append(matrix.Movie8.id)
        movies_id.append(matrix.Movie9.id)
        movies_id.append(matrix.Movie10.id)

        movies = Movie.objects.filter(id__in=movies_id)
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    else:
        # EM을 기준으로 합시다 > KNN, EM, K 일때 여기로 들어옴.
        data_scaled = StandardScaler().fit_transform(data_slice)
        df_end = pd.DataFrame(data_scaled)
        model = GaussianMixture(n_components=cluster_n, max_iter=20, random_state=0, covariance_type='spherical').fit(df_end)
        y_predict = model.fit_predict(df_end)

    # print(y_predict)

    ## 4. 나의 넘버(y_predict[-1]를 통해 클러스터링 영화들을 가져옵니다.)
    cluster_number = y_predict[-1]
    # print(cluster_number)
    cluster_movies = [int(df[x:x+1].values[0][0]) for x in range(len(y_predict)-1) if y_predict[x]==y_predict[-1]]

    # cluster_movies = [data_slice[x:x+1].values[0][1] for x in range(len(y_predict)-1) if y_predict[x]==y_predict[-1]]
    # print(cluster_movies)
    pick_movies = random.sample(cluster_movies, k=10)
    movies = Movie.objects.filter(id__in=pick_movies).order_by('-watch_count')
    serializer = MovieSerializer(movies, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
