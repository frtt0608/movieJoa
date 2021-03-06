from django.urls import path
from api.views import movie_views
from api.views import auth_views
from api.views import rate_views
from api.views import user_views
from api.views import admin_views

from api.views import Kmeans_views
from api.views import Hcluster_views
from api.views import EMcluster_views

from api.views import cluster_views
from api.views import IMDB_views
from api.views import subscription_views
from api.views import matrix_views
from api.views import brightics_views
from api.views import KNN_views

urlpatterns = [
    # user 관리
    path('auth/signup/', auth_views.signup, name='sign_up'),
    path('auth/signin/', auth_views.signin, name='sign_in'),
    path('auth/userState/', auth_views.userstate, name='user_state'),
    path('auth/logout/', auth_views.logout, name='logout'),

    path('movies/', movie_views.movies, name='movie_list'),
    path('movies/<int:movie_id>', movie_views.detail, name='movie_datail'),
    path('movies/<int:movie_id>/<int:profile_id>/', movie_views.getrate, name='movie_getrate'),
    path('movies/homepage/', movie_views.homepage, name='movie_homepage'),

    path('users/', user_views.users, name='user_list'),
    path('users/<int:user_id>', user_views.detail, name='user_detail'),
    path('user/<int:user_id>/movies/', user_views.userMovie),

    # parse_data / rating 관련
    path('ratings/', rate_views.ratings, name='rate_list'),

    # search 관련
    path('genres/', movie_views.genres, name="movies_by_genre"),
    path('ages/', movie_views.ages, name="movies_by_age"),
    path('occupations/', movie_views.occupations, name="movies_by_occupation"),
    path('genders/', movie_views.genders, name="movies_by_gender"),

    # user 및 movie UD
    path('movie/<int:movie_pk>/update/', admin_views.movie_update, name='movie_update'),
    path('movie/<int:movie_pk>/delete/', admin_views.movie_delete, name='movie_delete'),
    path('profile/<int:user_pk>/update/', admin_views.profile_update, name='profile_update'),
    path('profile/<int:user_pk>/delete/', admin_views.profile_delete, name='profile_delete'),

    # cluster 관련 정보를 조회, 변경합니다.
    path('cluster/', cluster_views.cluster, name='cluster'),
    path('subscription/create/', subscription_views.create, name='subscription_create'),
    path('subscription/manager/', subscription_views.manager, name="subscription_manager"),
    path('subscription/itembasedmovies/<int:profile_pk>', subscription_views.itembased_movies, name="subscription_itembasedmovies"),
    path('subscription/userbasedmovies/<int:profile_pk>', subscription_views.userbased_movies, name="subscription_userbasedmovies"),
    path('subscription/itembasedmovies2/<int:profile_pk>', subscription_views.itembased_movies2, name="subscription_itembasedmovies2"),

    # KNN 알고리즘
    path('KNN/movie/', KNN_views.KNN_algorithm_movie),
    path('KNN/user/', KNN_views.KNN_algorithm_user),
    path('KNN/checkCSV/', KNN_views.checkCSV),

    # Rating CRUD
    path('movie/<int:movie_pk>/score/cdu/', rate_views.cduRating),
    path('signup/new_cluster/', auth_views.new_cluster)
]
