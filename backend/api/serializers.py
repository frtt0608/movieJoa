from django.contrib.auth.models import User
from .models import Profile, Movie, Rate, Subscription_manager
from rest_framework import serializers
from django.db.models import Avg

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.SerializerMethodField('get_username')
    is_staff = serializers.SerializerMethodField('get_is_staff')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'is_staff', 'gender', 'age', 'occupation', 'approval', 'subscription')

    def get_username(self, obj):
        return obj.user.username

    def get_is_staff(self, obj):
        return obj.user.is_staff

class MovieSerializer(serializers.ModelSerializer):
    genres_array = serializers.SerializerMethodField('get_genres_array')
    averagerate = serializers.SerializerMethodField('get_averagerate')
    castings = serializers.SerializerMethodField('get_castings')
    

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'watch_count', 'score_users', 'averagerate','plot','url','director','castings')
        # fields = ('id', 'title', 'genres_array', 'watch_count', 'score_users', 'averagerate','plot','url','director')

    def get_castings(self, obj):
        casting = Movie.objects.get(id=obj.id).casting
        if casting.count('|') >= 3:
            casting = casting.split('|')
            casting = '|'.join(casting[:3])
        return casting

    def get_averagerate(self, obj):

        ## version 1
        average_rate = Rate.objects.filter(MovieID=obj.id).aggregate(Avg('rating'))
        if average_rate['rating__avg']!=None:
            return round(average_rate['rating__avg'], 2)
        else:
            return 0
        ##
    def get_genres_array(self, obj):
        return '|'.join(obj.genres_array)
        ## version 2
        # result = 0
        # count = 0
        # movie = Movie.objects.get(pk=obj.id)
        # rates = movie.rate_set.all()
        # for rate in rates:
        #     count += 1
        #     result += rate.rating
        # # print(type(obj.id), '2') 이건 그거 자체
        # if count==0:
        #     return 0
        # else:
        #     print(result/count, obj.title)
        #     return result/count

class Movie_Genre_Serializer(serializers.ModelSerializer):
    genres_array = serializers.SerializerMethodField('get_genres_array')
    averagerate = serializers.SerializerMethodField('get_averagerate')
    castings = serializers.SerializerMethodField('get_castings')
    

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'watch_count', 'score_users', 'averagerate','plot','url','director','castings')
        # fields = ('id', 'title', 'genres_array', 'watch_count', 'score_users', 'averagerate','plot','url','director')

    def get_castings(self, obj):
        casting = Movie.objects.get(id=obj.id).casting
        if casting.count('|') >= 3:
            casting = casting.split('|')
            casting = '|'.join(casting[:3])
        return casting

    def get_averagerate(self, obj):

        ## version 1
        average_rate = Rate.objects.filter(MovieID=obj.id).aggregate(Avg('rating'))
        if average_rate['rating__avg']!=None:
            return round(average_rate['rating__avg'], 2)
        else:
            return 0

    def get_genres_array(self, obj):
        return '|'.join(obj.genres_array)


class Movie_Age_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    title = serializers.SerializerMethodField('get_title')
    genres_array = serializers.SerializerMethodField('get_genres_array')
    watch_count = serializers.SerializerMethodField('get_watch_count')
    averagerate = serializers.SerializerMethodField('get_averagerate')
    plot = serializers.SerializerMethodField('get_plot')
    url = serializers.SerializerMethodField('get_url')
    director = serializers.SerializerMethodField('get_director')
    casting = serializers.SerializerMethodField('get_casting')
    class Meta:
        model = Movie
        # fields = ('id', 'title', 'genres_array', 'watch_count', 'averagerate')
        fields = ('id', 'title', 'genres_array','watch_count','averagerate', 'plot','url','director','casting')
    def get_id(self, obj):
        return obj['MovieID']
    def get_title(self, obj):
        return obj['MovieID__title']
    def get_genres_array(self, obj):
        return obj['MovieID__genres']
    def get_watch_count(self, obj):
        return obj['MovieID__watch_count']
    def get_averagerate(self, obj):
        return obj['rating__avg']

    def get_plot(self, obj):
        return obj['MovieID__plot']
    def get_url(self, obj):
        return obj['MovieID__url']
    def get_director(self, obj):
        return obj['MovieID__director']
    def get_casting(self, obj):
        tmp = obj['MovieID__casting']
        if tmp.count('|') >= 3:
            tmp = tmp.split('|')
            tmp = '|'.join(tmp[:3])
        return tmp
        # return obj['MovieID__casting']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields =  "__all__"
        fields = ('id', 'username')

class SubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Subscription_manager
        # fields =  "__all__"
        fields = ('id', 'Profile', 'request', 'approval', 'request_day', 'apply_day', 'username')

    def get_username(self, obj):
        profile = obj.Profile
        user = User.objects.get(pk=profile.user_id)
        # print(username.__dict__, '떳냐아')
        return user.username
