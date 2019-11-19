from django.contrib import admin
from .models import Profile, Movie, Rate, Cluster, Matrix
from .models import User_Cluster_Hmeans, Movie_Cluster_Hmeans
from .models import User_Cluster_Kmeans, Movie_Cluster_Kmeans
from .models import User_Cluster_EM, Movie_Cluster_EM
from .models import Subscription_manager
#
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'gender', 'age','occupation', 'approval', 'subscription']
class MovieAdmin(admin.ModelAdmin):
   list_display = ['id', 'title', 'genres', 'watch_count', 'plot', 'url']
class RateAdmin(admin.ModelAdmin):
   list_display = ['id', 'UserID', 'MovieID', 'rating', 'Timestamp']
# cluster
class UserHAdmin(admin.ModelAdmin):
   list_display = ['id', 'UserID', 'H3', 'H4', 'H5', 'H6', 'H7']
class MovieHAdmin(admin.ModelAdmin):
   list_display = ['id', 'MovieId', 'H3', 'H4', 'H5', 'H6', 'H7']
class Movie_Cluster_KmeansAdmin(admin.ModelAdmin):
   list_display = ['id', 'MovieId', 'K3', 'K4', 'K5', 'K6', 'K7']
class User_Cluster_KmeansAdmin(admin.ModelAdmin):
   list_display = ['id', 'UserID', 'K3', 'K4', 'K5', 'K6', 'K7']
class ClusterAdmin(admin.ModelAdmin):
   list_display = ['id', 'n_component', 'way']
class UserEMAdmin(admin.ModelAdmin):
   list_display = ['id', 'UserID', 'EM3', 'EM4', 'EM5', 'EM6', 'EM7']
class MovieEMAdmin(admin.ModelAdmin):
   list_display = ['id', 'MovieId', 'EM3', 'EM4', 'EM5', 'EM6', 'EM7']
class Subscription_managerAdmin(admin.ModelAdmin):
    list_display = ['id', 'Profile', 'request', 'approval', 'request_day', 'apply_day']
class MatrixAdmin(admin.ModelAdmin):
   list_display = ['UserID', 'Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6', 'Movie7', 'Movie8', 'Movie9', 'Movie10']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Matrix, MatrixAdmin)
# cluster
admin.site.register(User_Cluster_Kmeans, User_Cluster_KmeansAdmin)
admin.site.register(Movie_Cluster_Kmeans, Movie_Cluster_KmeansAdmin)
admin.site.register(User_Cluster_Hmeans, UserHAdmin)
admin.site.register(Movie_Cluster_Hmeans, MovieHAdmin)
admin.site.register(User_Cluster_EM, UserEMAdmin)
admin.site.register(Movie_Cluster_EM, MovieEMAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Subscription_manager, Subscription_managerAdmin)
