<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 by 영화이름-->
      <v-col>
        <v-flex>
          <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">User Profile</p>
          <p class="profile"><span style="margin-right: 1rem; font-weight: bold;">name</span><span>{{ user.username }}</span></p>
          <p class="profile"><span style="margin-right: 1rem; font-weight: bold;">gender</span><span>{{ user.gender }}</span></p>
          <p class="profile"><span style="margin-right: 1rem; font-weight: bold;">age</span><span>{{ user.age }}</span></p>
          <p class="profile" style="margin-bottom: 3rem;"><span style="margin-right: 1rem; font-weight: bold;">occupation</span><span>{{ user.occupation }}</span></p>
          <v-btn color="red lighten-2" dark style="margin-right: 1rem;" @click="dialog=true">Edit</v-btn>
          <v-btn color="lighten-2" dark @click="userMovie(); movie_show=!movie_show">내가봤던 영화</v-btn>
          <p v-show="movie_show" v-if="movielist.length < 1">보신 영화가 없습니다..</p>
          <v-layout v-show="movie_show" v-if="movielist.length > 1" row pa-5>
            <v-flex>
              <carousel :per-page="pageNum">
                <slide v-for="(movie,index) in movielist" :key="index" style="height: 22rem; width: 15rem;">
                  <v-card style="margin:10px; height: 21rem; width: 15rem; border-radius:15px;" color="#424242" dark>
                    <v-img contain :src="movie.url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
                    <v-card-text>
                      <div class="movietitle">
                        {{ movie.title.substring(0, movie.title.indexOf("(")) }}<br>
                        <span class="hovertext" style="vertical-align: middle;">{{ movie.title.substring(0, movie.title.indexOf("(")) }}</span>
                      </div>
                      <i class="fas fa-star" style="color: #FFB600; margin-right: 0.5rem;" /><span>평점 </span><span style="font-weight: bold;">{{ movie.averagerate }}</span>
                      <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_MovieDetail(movie)">explore</v-btn>
                    </v-card-text>
                  </v-card>
                </slide>
              </carousel>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex>
          <div v-if="typeof(profile_data[1])!='boolean'" style="margin-top: 3rem;">
            <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">Similar Users</p>
            <carousel :per-page="pageNum">
              <slide v-for="person in profile_data.slice(1, 6)" :key="person.username" style="height: 13rem; width: 15rem;">
                <v-card style="margin:10px; border-radius:15px;" color="#424242" dark>
                  <v-card-text>
                    <v-container>
                      <p style="color: white; font-size: 1.4rem;">{{ person.username }}</p>
                      {{ person.age }} / {{ person.gender }}<br>
                      {{ person.occupation }}<br>
                      <v-btn text color="primary" @click="SELECT_UserDetail(person.id, person.username)">explore</v-btn>
                    </v-container>
                  </v-card-text>
                </v-card>
              </slide>
            </carousel>
          </div>
          <div v-else style="margin-top: 3rem;">
            <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">Similar Users</p>
            <p class="profile">
              <span style="margin-right: 1rem; font-weight: bold;">영화 평점을 등록해주세요!</span>
            </p>
          </div>
        </v-flex>
      </v-col>
    </v-layout>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Profile Edit</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <!-- <v-text-field
              v-model="username"
              :counter="10"
              label="Name"
              :rules="nameRules"
              required
            /> -->
            <v-layout>
              <span style="vertical-align: middle; color: rgba(0, 0, 0, 0.54); padding-left: 0.3rem; padding-right: 2.5rem;">Gender</span>
              <v-radio-group v-model="user.gender" row>
                <v-radio label="Female" value="F" />
                <v-radio label="Male" value="M" />
              </v-radio-group>
            </v-layout>
            <v-text-field
              v-model="age"
              type="number"
              label="Age"
              :rules="ageRules"
              required
            />
            <v-select
              v-model="occupation"
              :items="occupations"
              label="Occupation"
              :rules="occupationRules"
              required
            />
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          <v-btn v-if="ageRules[0](age)===true && occupationRules[0](occupation)===true" text @click="dialog = false; edit()">Save</v-btn>
          <v-btn v-else disabled color="dark darken-1" text @click="dialog = false; edit()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import router from "../../router";
import axios from 'axios'
import { Carousel, Slide } from 'vue-carousel';

export default {
  components: {
    Carousel,
    Slide
  },
  data: () => ({
    user: null,
    username: null,
    age: null,
    gender: null,
    occupations: ["other","academic/educator","artist","clerical/admin","college/grad student",
    "customer service","doctor/health care","executive/managerial","farmer","homemaker",
    "K-12 student","lawyer","programmer","retired","sales/marketing","scientist",
    "self-employed","technician/engineer","tradesman/craftsman","unemployed","writer"],
    occupation: null,
    profile_data:'',
    dialog: false,
    modal: false,
    checkCSV: false,
    movie_show: false,
    pageNum: 4,
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length <= 10) || 'Name must be less than 10 characters'
    ],
    ageRules: [
      function(v) {
        if (!v) {
          return 'Age is required'
        }
        if (v <= 0) {
          return 'Age must be more than 0'
        }
        return !!v
      }
    ],
    occupationRules: [
      function(v) {
        if (!v) {
          return 'occupation is required'
        }
        return !!v
      }
    ],
    user_data:'',
    subscription_date:'',
    now_date:'',
    movielist:[],
  }),
  created() {
    if (this.$session.get('id')=="") {
      this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '로그인을 해주세요!',
        })
        router.push({name:"sign-in"})
    } else {
      this.fetchdata();
    }
  },
  methods: {
    async fetchdata() {
      this.user = this.$session.get('id')
      const apiUrl = '/api'
      const id = this.$session.get('id_number')
      var profile = await axios.get(`${apiUrl}/users/${id}`)
      this.profile_data = profile.data

      // 구독 날짜 확인하기,
      // 오늘 날짜 : this.now_date , ex) 20190910
      // 회원의 구독 날짜 : this.subscription_date, ex) 20190801
      this.user_data = this.profile_data[0]
      this.subscription_date = this.user_data.subscription.substring(0, 10).replace(/-/g,'')
      var now = new Date()
      var year = now.getFullYear()
      var month = now.getMonth() + 1
      var date = now.getDate()
      if ( month < 10 ) {
        month = '0' + String(month)
      } else {
        month = String(month)
      }
      if ( date < 10) {
        date = '0' + String(date)
      } else {
        date = String(date)
      }
      this.now_date = String(year)+month+date
      this.user = this.profile_data[0]
      this.username = this.user.username
      this.age = this.user.age
      this.gender = this.user.gender
      this.occupation = this.user.occupation
    },
    SELECT_UserDetail(id, username) {
      var user_data = {'id':id, 'username':username}
      router.push({name:'user-detail', params : {'id':user_data.id, 'user_data':user_data}})
    },
    userMovie() {
      const apiUrl = '/api'
      let user_pk = this.$session.get('id_number')
      axios.post(`${apiUrl}/user/${user_pk}/movies/`).then(res => {
        this.movielist = res.data
      })
    },
    NewRate() {
      const apiUrl = '/api'
      axios.post(`${apiUrl}/KNN/checkCSV/`,{
        pk:this.$session.get('id_number')
      }).then(res => {
        if(res.data==false)
          this.modal = !(this.modal)
        else
          this.$swal.fire({
            text: '이미 등록한 평점이 있어요.'
          })
      })
    },
    async edit() {

      let __this = this;
      const id = this.$session.get('id_number');
      const apiUrl = '/api';
      await axios.post(`${apiUrl}/users/${id}`, {
        username: __this.username,
        gender: __this.gender,
        age: __this.age,
        occupation: __this.occupation
      }).then(() => {
        var profile = axios.get(`${apiUrl}/users/${id}`)
        this.profile_data = profile.data
        this.user = this.profile_data[0]
      })
    },
    SELECT_MovieDetail(movie) {
      var movie_data = {'id':movie.id, 'title':movie.title, 'genres_array':movie.genres_array,
                  'watch_count' : movie.watch_count, 'score_users':movie.score_users, 'averagerate':movie.averagerate,
                  'plot':movie.plot,'url':movie.url,'director':movie.director,'casting':movie.casting}
      router.push({name:'movie-detail', params : {'id':movie_data.id}})
    }
  }
}
</script>
<style scoped>
  .profile {
    color:  rgba(255, 255, 255, 0.7);
    font-size: 2rem;
  }
</style>
