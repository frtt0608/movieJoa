# 빅데이터 스켈레톤(2주차)

## 목차

1. Clone, Setting
2. User Edit 
3. Subscription



## 1. Clone, Setting

### (1) Clone

- Git clone (~/)

  ```bash
  $ git clone https://lab.ssafy.com/Kim-Seul-Gi/bigdata-sub1.git
  ```

### (2) Setting

- Backend ( ~/bigdata-sub1/backend)

  ```bash
  $ pip install -r requirements.txt
  $ python manage.py makemigraions
  $ python manage.py migrate
  $ python manage.py runserver
  ```

- Frontend ( ~/bigdata-sub1/frontend)

  ```bash
  $ npm install
  $ npm run serve
  ```



## 2. User Edit 

### (1) POST요청 (http://127.0.0.1:8000)

```python
# user_views.py

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def detail(request, user_id):
    user = User.objects.get(pk=user_id)
    user_profile = Profile.objects.get(user=user)
    # ...
    
    elif request.method == 'POST':
        user_profile.username = request.data.get('username', None)
        user_profile.age = request.data.get('age', None)
        user_profile.gender = request.data.get('gender', None)
        user_profile.occupation = request.data.get('occupation', None)
        user_profile.save()
        return Response(status=status.HTTP_200_OK)
    
```

- mypage 내 edit 버튼을 누르면 modal 형태로 된 form 수정이 가능하도록 함

```javascript
// edit 버튼을 눌렀을 때

async edit() {
      let __this = this;
      const id = this.$session.get('id_number');
      const apiUrl = '/api';
      let tmp = await axios.post(`${apiUrl}/users/${id}`, {
        username: __this.username,
        gender: __this.gender,
        age: __this.age,
        occupation: __this.occupation
      }).then(async res => {
        var profile = await axios.get(`${apiUrl}/users/${id}`)
        this.profile_data = profile.data
        this.user = this.profile_data[0]
      })
    }

#  wrapper for create user Profile
def create_profile(**kwargs):

    user = User.objects.create_user(
        username=kwargs['username'],
        password=kwargs['password'],
        is_active=True
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

    score_users = models.ManyToManyField(User, through='Rate', related_name='score_movies')

    @property
    def genres_array(self):
        return self.genres.strip().split('|')

    def __str__(self):
        return f'{self.title}'

class Rate(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rate")
    MovieID = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="user_movie")
    rating = models.IntegerField(default=0)
    Timestamp = models.IntegerField()
```



## 3. Subscription

### (1) model 정의

```python
# models.py

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='M')
    age = models.IntegerField(default=25)
    occupation = models.CharField(max_length=200)
    approval = models.BooleanField(default=False)
    subscription = models.DateTimeField(default=datetime.datetime.now() - datetime.timedelta(days=1))

class Subscription_manager(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_sub")
    request = models.IntegerField(default=0)
    approval = models.BooleanField(default=False)
    request_day = models.DateTimeField(auto_now_add=True)
    apply_day = models.DateTimeField(auto_now=True)

    # ...
```

### (2) back end

```python
# subscription_views.py

# ...
@api_view(['POST'])
def create(request):
    if request.method == 'POST':

    # Subscription_manager 이라는 모델에 생성을 해야 한다.
        username = request.data.get('user')
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        check_subscription_request = Subscription_manager.objects.filter(Profile=profile, approval=False)
        if check_subscription_request:
            message = {'message':'이미 구독 신청을 한 상태입니다.'}
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            subscription_request = Subscription_manager.objects.create(
                Profile=profile,
                request=request.data.get('request'),
                approval=False,
            )
            return Response(status=status.HTTP_200_OK)

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
```

- 유저 검색
  - 유저 이름을 통해 검색하기 가능
  - 엔터 클릭, search 로 가능
  - 순서나열은 따로 적용하지 않음
  - 카드를 누르면 유저 프로필 페이지로 이동
