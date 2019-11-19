<template>
  <v-container class="pa-2" fluid grid-list-md>
    <v-layout column>
      <v-flex v-if="user != 'admin'">
        <div v-if="approval" class="mx-auto">
          <v-card v-if="before_extend" color="#424242" dark class="mx-3 my-3 px-8 py-3">
            <v-card-title style="font-size: 1.2rem;">{{ user }}님의 구독 유효 기간 <span style="padding-left: 0.7rem;">{{ subdate }}</span></v-card-title>
            <v-card-text>
              <v-radio-group v-model="picked_amount" style="display:inline-block;" row>
                <v-radio value="30" label="30 days" color="" />
                <v-radio value="90" label="90 days" color="" />
              </v-radio-group>
              <v-btn style="margin-left: 0.7rem;" @click="extend_subscription()">구독 연장</v-btn>
            </v-card-text>
          </v-card>
          <v-card v-else color="#424242" dark class="mx-3 my-3  px-3 py-3">
            <v-card-text>연장 신청이 완료되었어요. 관리자 승인 중입니다. :)</v-card-text>
          </v-card>
          <div id="item">
            <span style="color: white; font-size: 1.7rem; margin-left: 0.9rem; font-family: 'Jua', sans-serif;"><v-icon size="2rem" color="white">mdi-movie</v-icon> {{ user }}님을 위한 영화 추천</span>
          </div>
          <v-layout row wrap>
            <v-flex v-if="this.$store.state.data.movieList_homepage_itembased.length!=0">
              <carousel :per-page="pageNum">
                <slide v-for="(movie, index) in this.$store.state.data.movieList_homepage_itembased" :key="index" style="height: 22rem; width: 15rem;">
                  <v-card style="margin:10px; height: 21rem; width: 15rem; border-radius:15px;" color="#424242" dark class="rounded-card">
                    <v-img :src="movie.url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
                    <v-card-text>
                      <div class="movietitle">
                        {{ movie.title.substring(0, movie.title.indexOf("(")) }}<br>
                        <span class="hovertext" style="vertical-align: middle;">{{ movie.title.substring(0, movie.title.indexOf("(")) }}</span>
                      </div>
                      <i class="fas fa-star" style="color: #FFB600; margin-right: 0.5rem;" />
                      <span>평점 </span>
                      <span style="font-weight: bold;">{{ movie.averagerate }}</span>
                      <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_MovieDetail(movie)">explore</v-btn>
                    </v-card-text>
                  </v-card>
                </slide>
              </carousel>
            </v-flex>

            <v-flex v-else>
              <div style="margin-top: 3rem;">
                <p class="profile">
                  <span style="margin-right: 1rem; font-weight: bold;">영화 평점을 등록해주세요!</span>
                </p>
                <p>
                  <v-btn color="red lighten-2" dark style="margin-bottom: 1rem;" to="/choices/">평가하러 가기</v-btn>
                </p>
              </div>
            </v-flex>
          </v-layout>
          <div id="user">
            <span style="color: white; font-size: 1.7rem; margin-left: 0.9rem; font-family: 'Jua', sans-serif;"><v-icon size="2rem" color="white">mdi-movie</v-icon> 유사한 사용자의 선호 영화</span>
          </div>
          <v-layout row wrap>
            <v-flex v-if="this.$store.state.data.movieList_homepage_userbased.length!=0">
              <carousel :per-page="pageNum">
                <slide v-for="(movie, index) in this.$store.state.data.movieList_homepage_userbased" :key="index" style="height: 22rem; width: 15rem;">
                  <v-card style="margin:10px; height: 21rem; width: 15rem; border-radius:15px;" color="#424242" dark>
                    <v-img :src="movie.url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
                    <v-card-text>
                      <div class="movietitle">
                        {{ movie.title.substring(0, movie.title.indexOf("(")) }}<br>
                        <span class="hovertext">{{ movie.title.substring(0, movie.title.indexOf("(")) }}</span>
                      </div>
                      <i class="fas fa-star" style="color: #FFB600; margin-right: 0.5rem;" /><span>평점 </span><span style="font-weight: bold;">{{ movie.averagerate }}</span>
                      <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_MovieDetail(movie)">explore</v-btn>
                    </v-card-text>
                  </v-card>
                </slide>
              </carousel>
            </v-flex>

            <v-flex v-else>
              <div style="margin-top: 3rem;">
                <p class="profile">
                  <span style="margin-right: 1rem; font-weight: bold;">영화 평점을 등록해주세요!</span>
                </p>
                <p>
                  <v-btn color="red lighten-2" dark style="margin-bottom: 1rem;" to="/choices/">평가하러 가기</v-btn>
                </p>
              </div>
            </v-flex>
          </v-layout>
        </div>

        <div v-else class="mx-auto">
          <v-card v-if="before_create" color="#424242" dark class="mx-3 my-3 px-8 py-3">
            <v-card-text>
              <p style="font-size: 1rem; text-align: left;">{{ user }}님은 구독 서비스를 이용한 적이 없어요.</p>
              <p style="font-size: 1rem; text-align: left;">영화 추천을 위한 구독을 원하시나요?</p>
              <v-radio-group v-model="picked_amount" style="display:inline-block;" row>
                <v-radio value="30" label="30 days" color="" />
                <v-radio value="90" label="90 days" color="" />
              </v-radio-group>
              <v-btn style="margin-left: 0.7rem;" @click="create_subscription()">구독 신청</v-btn>
            </v-card-text>
          </v-card>
          <v-card v-else color="#424242" dark class="mx-3 my-3 px-3 py-3">
            <v-card-text>구독 신청이 완료되었어요. 관리자 승인 중입니다 :)</v-card-text>
          </v-card>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import axios from 'axios';
import router from "../router";
import { Carousel, Slide } from 'vue-carousel';

export default {
  components:{
    Carousel,
    Slide
  },
  props : {
    profiledata : {
      type : Array,
      default: () => new Array()
    },
    nowdate : {
      type : String,
      default: ''
    },
    user : {
      type : String,
      default: ''
    },
    subdate : {
      type : String,
      default: ''
    },
    approval : {
      type : Boolean,
      default: true
    },
  },
  data: () => ({
    amounts: [30, 90],
    picked_amount:'',
    before_create : true,
    before_extend : true,
    userbased_movies:'',
    itembased_movies:'',
    pageNum: 4
  }),
  watch: {
    profiledata() {
      const params = {
        id : this.$session.get('id_number'),
        approval : this.profiledata[0].approval,
        resemble_users : this.profiledata.slice(1)
      }
      this.getMovies_subscription_itembased(params)
      this.getMovies_subscription_userbased(params)
    }
  },
  methods : {
    ...mapActions("data", ["getMovies_subscription_itembased", "getMovies_subscription_userbased"]),
    async create_subscription() {
      const apiUrl = '/api'
      var subscription = await axios.post(`${apiUrl}/subscription/create/`, {user : this.$session.get('id'), request:this.picked_amount})
      if (subscription.data.create) {
        this.$swal.fire({
            title: '구독 신청 완료!',
            type: 'success'
          })
      } else {
          this.$swal.fire({
            type: 'error',
            title: 'Oops...',
            text: '이미 구독을 신청한 상태입니다!',
          })
      }
      this.before_create = false
    },
    async extend_subscription() {
      const apiUrl = '/api'
      var subscription = await axios.post(`${apiUrl}/subscription/create/`, {user : this.$session.get('id'), request:this.picked_amount})
      if (subscription.data.create) {
        this.$swal.fire({
            title: '구독 신청 완료!',
            type: 'success'
          })
      } else {
          this.$swal.fire({
            type: 'error',
            title: 'Oops...',
            text: '이미 구독을 신청한 상태입니다!',
          })
      }
      this.before_extend = false
    },
    SELECT_MovieDetail(movie) {
      var movie_data = {'id':movie.id, 'title':movie.title, 'genres_array':movie.genres_array,
                  'img':movie.img,'watch_count' : movie.watch_count, 'score_users':movie.score_users, 'averagerate':movie.averagerate,
                  'plot':movie.plot,'url':movie.url,'director':movie.director,'casting':movie.casting}

      router.push({name:'movie-detail', params : {'id':movie_data.id, 'movie_data':movie_data}})
      window.location.reload()
    }
  }
}
</script>
<style>
  .movietitle {
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
  }
  .movietitle .hovertext {
    visibility: hidden;
    /* width: 250px; */
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    bottom: 20%;
    white-space:normal;
    /* Position the tooltip */
    position: absolute;
    z-index: 1;
  }
  .movietitle:hover .hovertext {
    visibility: visible;
  }
</style>
<style scoped>
  .profile {
    color:  rgba(255, 255, 255, 0.7);
    font-size: 2rem;
  }
</style>
