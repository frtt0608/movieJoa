<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 by 영화이름-->
      <v-flex>
        <div style="color:rgb(255,255,255)">No. {{ movie_data[0].id }}</div>
        <v-card class="mx-auto" max-width="600px" color="#424242" dark>
          <v-img :src="movie_data[0].url" height="400px" contain />
          <v-col>
            <h1>{{ movie_data[0].title }}</h1>
            <div v-if="$session.get('id_number')!=''">
              <v-btn v-if="!rate_flag" icon @click="rate_show=!rate_show">{{ rate_show ? 'cancel' : '평점 남기기' }}</v-btn>
              <v-btn v-if="rate_flag" icon @click="rate_show=!rate_show; score=tmp_score ">{{ rate_show ? 'cancel' : '평점 수정하기' }}</v-btn>
            </div>
            <v-flex v-show="rate_show">
              <div class="mx-auto" style="width:200px">
                <!-- <v-text-field
                  v-model="score"
                  label="score"
                  :rules="scoreRules"
                  type="number"
                  required
                /> -->
                내가 남긴 평점 : {{score}}
                <v-rating
                  v-model="score"
                  label="score"
                  color="yellow darken-3"
                  background-color="grey darken-1"
                  half-increments
                  hover
                />

                <v-btn v-if="!rate_flag" @click="createRating(movie_data[0].id)">등록</v-btn>
                <v-btn v-if="rate_flag" @click="deleteRating(movie_data[0].id)">삭제</v-btn>
                <v-btn v-if="rate_flag" @click="updateRating(movie_data[0].id)">수정</v-btn>
                <!-- <v-btn @click="rate_show = !rate_show; score=tmp_score">취소</v-btn> -->
              </div>
            </v-flex>
            <div class="grey--text">평점 : {{ movie_data[0].averagerate }} , 조회수 : {{ movie_data[0].watch_count }}</div>
            <div class="grey--text">Director: {{ movie_data[0].director }}</div><br>
            <div class="grey--text" v-for="(genre, i) in this.genreList" v-bind:key="i">{{genre}}</div>
          </v-col>
          <br>
          <v-btn icon @click="show = !show">
            <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
          <v-expand-transition>
            <div v-show="show">
              <p style="font-size: 1.5rem; color: white; font-family: 'Jua', sans-serif;">출연배우</p>
              <div v-for="(casting, i) in this.castingList" v-bind:key="i">
              <span class="grey--text" style="font-family: 'Jua', sans-serif;">
                {{casting}}</span>
              </div>
              <p style="font-size: 1.5rem; color: white; font-family: 'Jua', sans-serif;"
                  >줄거리</p>
              <v-card-text>{{ movie_data[0].plot }}</v-card-text> 
            </div>
          </v-expand-transition>
        </v-card>
        <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">Similar Movies</p>
      </v-flex>
      <v-flex>
        <carousel :per-page="4">
          <slide v-for="(movie, index) in movie_data.slice(1)" :key="index" style="height: 22rem; width: 15rem;">
            <v-card style="margin:10px; height: 21rem; width: 15rem; border-radius:15px;" color="#424242" dark>
              <v-img contain :src="movie.url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
              <v-card-text>
                <div class="movietitle2" style="margin-left:0.3rem;">
                  <!-- {{ movie.title.substring(0, movie.title.indexOf("(")) }}<br>
                  <span class="hovertext">{{ movie.title.substring(0, movie.title.indexOf("(")) }}</span> -->
                  <span>{{ movie.title }}</span>
                  <span style="margin-right:0.5rem;">{{ movie.title }}</span>
                </div>
                <i class="fas fa-star" style="color: #FFB600; margin-right: 0.5rem;" /><span>평점 </span><span style="font-weight: bold;">{{ movie.averagerate }}</span>
                <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_MovieDetail(movie)">explore</v-btn>
              </v-card-text>
            </v-card>
          </slide>
        </carousel>
      </v-flex>
    </v-layout>
    <v-btn @click="search()">검색으로 이동</v-btn>
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
  props: {
    id : {
      type: [Number, String],
      default: ''
    },
  },
  data: () => ({
    score: 0.0,
    show: false,
    rate_show: false,
    castingList: [],
    genreList: [],
    movie_data:[
      {"id":''},
      {"averagerate":''},
      {"castings":''},
      {"director":''},
      {"genres_array":''},
      {"plot":''},
      {"score_users":''},
      {"title":''},
      {"url":''},
      {"watch_count":''}
    ],
    rate_flag:false,
    tmp_score:0,
  }),
  mounted() {
    this.fetchdata()
  },
  methods: {
    async fetchdata() {
        const apiUrl = '/api'
        const id = this.$route.params.id
        var movie = await axios.get(`${apiUrl}/movies/${id}`)
        this.movie_data = movie.data
        this.castingList = this.movie_data[0].castings.split("|")
        this.genreList = this.movie_data[0].genres_array.split("|")
        if (this.$session.get('id_number')) {
          var myrate = await axios.get(`${apiUrl}/movies/${id}/${this.$session.get('id_number')}`)
          if (myrate.data.flag===true) {
            this.rate_flag = true
            this.score = myrate.data.rate
            this.tmp_score = this.score
          }
        }
    },
    search() {
      router.push({name:'movie-search'})
    },
    SELECT_MovieDetail(movie) {
      var movie_data = {'id':movie.id, 'title':movie.title, 'genres_array':movie.genres_array,
                  'img':movie.img,'watch_count' : movie.watch_count, 'score_users':movie.score_users, 'averagerate':movie.averagerate,
                  'plot':movie.plot,'url':movie.url,'director':movie.director,'casting':movie.casting}

      router.push({name:'movie-detail', params : {'id':movie_data.id, 'movie_data':movie_data}})
      window.location.reload()
    },
    createRating(id) {
      const apiUrl = '/api'
      axios.post(`${apiUrl}/movie/${id}/score/cdu/`, {
        user_pk:this.$session.get('id_number'),
        score:this.score
      }).then(res => {
        if(res.data==false) {
          this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '이미 평점을 등록하였습니다!',
        })
        } else {
          this.$swal.fire({
            title: '평점 등록 완료!',
            type: 'success'
          })
          this.tmp_score = this.score
        }
        this.rate_flag = !this.rate_flag
        this.rate_show = !this.rate_show
      })
    },
    updateRating(id) {
      const apiUrl = '/api'
      axios.put(`${apiUrl}/movie/${id}/score/cdu/`, {
        user_pk:this.$session.get('id_number'),
        score:this.score
      }).then(res => {
        if(res.data==false) {
          this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '등록한 평점이 없습니다!',
        })
        } else {
          this.$swal.fire({
            title: '평점 수정 완료!',
            type: 'success'
          })
          this.tmp_score = this.score
        }
        this.rate_show = !this.rate_show
      })
    },
    deleteRating(id) {
      const apiUrl = '/api'
      axios.delete(`${apiUrl}/movie/${id}/score/cdu/`, {
        data: {user_pk:this.$session.get('id_number')}
      }).then(res => {
        if(res.data==false) {
          this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '등록한 평점이 없습니다!',
        })
        } else {
          this.$swal.fire({
            title: '평점 삭제 완료!',
            type: 'success'
          })
          this.tmp_score = 0
          this.score = 0
        }
        this.rate_show = !this.rate_show
        this.rate_flag = !this.rate_flag
      })
    }
  }
};
</script>
<style scoped>
  .movietitle2 {
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
    text-align:left !important;
  }
  .movietitle2 .hovertext2 {
    visibility: hidden;
    /* width: 80%; */
    background-color: black;
    color: #fff;
    text-align: left;
    border-radius: 6px;
    padding: 5px;
    bottom: 20%;
    right:0px;
    white-space:normal;
    /* Position the tooltip */
    position: absolute;
    z-index: 1;
  }
  .movietitle2:hover .hovertext2 {
    visibility: visible;
  }
</style>
