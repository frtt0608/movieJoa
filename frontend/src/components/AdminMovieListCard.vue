<template>
  <div>
    <v-hover v-slot:default="{ hover }">
      <v-layout arow wrap text-left>
        <v-flex>
          <v-card style="margin:10px; height: 24rem; width: 15rem; border-radius:15px;" color="#424242" dark>
            <v-img :src="url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
            <v-card-text>
              <div class="movietitle">
                {{ title.substring(0, title.indexOf("(")) }}<br>
                <span class="hovertext2">{{ title.substring(0) }}</span>
              </div>
              <i class="fas fa-star" style="color: #FFB600;" /><span>평점 </span><span style="font-weight: bold;">{{ Math.round(averagerate*100)/100 }}</span>
              <span><v-btn text color="primary" @click="SELECT_MovieDetail()">explore</v-btn></span>
              <v-btn @click="movie_detail(id); dialog=true">수정</v-btn>
              <v-btn @click="movie_delete(id);">삭제</v-btn>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-hover>
    <v-dialog v-model="dialog" width="500">
      <v-card flat class="text-xs-center" min-width="500">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-card-text>
            <v-text-field
              id="title"
              v-model="tmp_title"
              hint="제목을 변경할 수 있습니다."
              name="title"
              label="Title"
              prepend-icon=""
              clearable
            />
            <v-select
              id="genres_array"
              v-model="tmp_genres_array"
              hint="장르를 변경할 수 있습니다."
              name="genres_array"
              label="Genres"
              :items="genres"
              attach
              genres_array
              multiple
            />
          </v-card-text>
        </v-form>
        <v-btn color="primary" text @click="movie_update(id); dialog=false">수정하기</v-btn>
        <v-btn color="primary" text @click="movie_cancel(); dialog=false">닫기</v-btn>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import router from "../router";
import axios from "axios"
export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: ""
    },
    genresarray: {
      type: String,
      default: ''
    },
    img: {
      type: String,
      default: ""
    },
    averagerate: {
      type: Number,
      default: 0.0
    },
    watchcount: {
      type: Number,
      default: 0
    },
    scoreusers: {
      type: Array,
      default: () => new Array()
    },
    plot: {
      type: String,
      default: ""
    },
    url: {
      type: String,
      default: ""
    },
    director: {
      type: String,
      default: ""
    },
    casting: {
      type: String,
      default: ""
    }
  },
  data: () => ({
    valid: true,
    dialog: false,
    genres: ['Action', 'Adventure', 'Animation', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', "Children's"],
    // genres_array : []
    tmp_genres_array : [],
    tmp_title : '',
  }),
  computed: {
    genresStr: function() {
      return this.genres_array.join(" / ");
    },
  },
  mounted() {
    this.tmp_genres = this.genres_array
  },
  methods: {
    SELECT_MovieDetail() {
      var movie_data = {'id':this.id, 'title':this.title, 'genres_array':this.genres_array,
                  'img':this.img,'watch_count' : this.watch_count, 'score_users':this.score_users, 'averagerate':this.averagerate,
                  'plot':this.plot,'url':this.url,'director':this.director,'casting':this.casting}
      router.push({name:'movie-detail', params : {'id':movie_data.id, 'movie_data':movie_data}})
    },
    movie_delete: function(id) {
      const apiUrl = '/api'
      let chk = confirm("정말 삭제하시겠습니까?")
      if (chk == true) {
        axios.delete(`${apiUrl}/movie/${id}/delete/`, {id})
        window.location.reload()
      }
    },
    movie_update: function(id) {
      const apiUrl = '/api'
      let chk = confirm("영화 정보를 변경하시겠습니까?")
      if(chk == true) {
        axios.put(`${apiUrl}/movie/${id}/update/`, {
          id:this.id,
          title:this.tmp_title,
          genres_array:this.tmp_genres_array
        })
      }
    },
    movie_detail: async function(id) {
      const apiUrl = '/api'
      var movie = await axios.get(`${apiUrl}/movies/${id}`)
      this.tmp_title = movie.data[0].title
      this.tmp_genres_array = movie.data[0].genres_array.split('|')
    },
    movie_cancel() {
      this.genres_array = this.tmp_genres
    }
  }
}
</script>

<style>
  .movietitle .hovertext2 {
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
  .movietitle:hover .hovertext2 {
    visibility: visible;
  }
</style>
