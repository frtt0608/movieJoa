from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='M')
    age = models.IntegerField(default=25)
    occupation = models.CharField(max_length=200)
    approval = models.BooleanField(default=False)
    subscription = models.DateTimeField(default=datetime.datetime(2019, 9, 10, 13, 47, 43, 630123))

class Subscription_manager(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_sub")
    request = models.IntegerField(default=0)
    approval = models.BooleanField(default=False)
    request_day = models.DateTimeField(auto_now_add=True)
    apply_day = models.DateTimeField(auto_now=True)

#  wrapper for create user Profile
def create_profile(**kwargs):
    user = User.objects.create_user(
        username=kwargs['username'],
        password=kwargs['password'],
        is_active=True,
    )

    profile = Profile.objects.create(
        user=user,
        gender=kwargs['gender'],
        age=kwargs['age'],
        occupation=kwargs['occupation']
    )

    return profile

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=500)
    watch_count = models.IntegerField(default=0)
    averagerate = models.IntegerField(default=0)
    plot = models.CharField(default='', max_length=1000)
    url = models.CharField(default='', max_length=500)
    director = models.CharField(default='', max_length=500)
    casting = models.CharField(default='', max_length=500)
    score_users = models.ManyToManyField(Profile, through='Rate', related_name='score_movies')

    @property
    def genres_array(self):
        return self.genres.strip().split('|')

    def __str__(self):
        return self.title

class Rate(models.Model):
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_rate")
    MovieID = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="profile_movie")
    rating = models.FloatField(default=0.0)
    Timestamp = models.IntegerField()

class Cluster(models.Model):
    n_component = models.IntegerField(default=0)
    way = models.CharField(max_length=50)

class Movie_Cluster_Kmeans(models.Model):
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_cluster_Kmeans")
    K3 = models.IntegerField(default=0)
    K4 = models.IntegerField(default=0)
    K5 = models.IntegerField(default=0)
    K6 = models.IntegerField(default=0)
    K7 = models.IntegerField(default=0)

class Movie_Cluster_Hmeans(models.Model):
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_cluster_Hmeans")
    H3 = models.IntegerField(default=0)
    H4 = models.IntegerField(default=0)
    H5 = models.IntegerField(default=0)
    H6 = models.IntegerField(default=0)
    H7 = models.IntegerField(default=0)

class Movie_Cluster_EM(models.Model):
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_cluster_EM")
    EM3 = models.IntegerField(default=0)
    EM4 = models.IntegerField(default=0)
    EM5 = models.IntegerField(default=0)
    EM6 = models.IntegerField(default=0)
    EM7 = models.IntegerField(default=0)

class User_Cluster_Kmeans(models.Model):
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_cluster_Kmeans")
    K3 = models.IntegerField(default=0)
    K4 = models.IntegerField(default=0)
    K5 = models.IntegerField(default=0)
    K6 = models.IntegerField(default=0)
    K7 = models.IntegerField(default=0)

class User_Cluster_Hmeans(models.Model):
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_cluster_Hmeans")
    H3 = models.IntegerField(default=0)
    H4 = models.IntegerField(default=0)
    H5 = models.IntegerField(default=0)
    H6 = models.IntegerField(default=0)
    H7 = models.IntegerField(default=0)

class User_Cluster_EM(models.Model):
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_cluster_EM")
    EM3 = models.IntegerField(default=0)
    EM4 = models.IntegerField(default=0)
    EM5 = models.IntegerField(default=0)
    EM6 = models.IntegerField(default=0)
    EM7 = models.IntegerField(default=0)

class Matrix(models.Model):
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="matrix_set")
    Movie1 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie1")
    Movie2 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie2")
    Movie3 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie3")
    Movie4 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie4")
    Movie5 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie5")
    Movie6 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie6")
    Movie7 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie7")
    Movie8 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie8")
    Movie9 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie9")
    Movie10 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie10")
