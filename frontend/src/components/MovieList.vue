<template>
  <v-container class="pa-2" fluid grid-list-md>
    <div v-if="this.$store.state.data.movieSearchList.length">
      {{ $store.state.data.movieSearchList.length }}개가 조회되었습니다.
      <!-- <v-btn @click="seemode_rate = false">조회 순</v-btn> -->
      <v-btn @click="seemode_rate = false">라이브러리 순</v-btn>
      <v-btn @click="seemode_rate = true">평점 순</v-btn>
    </div>
    <!-- <div v-else style="color: white">
      영화가 없어요!!!
    </div> -->
    <v-layout row wrap>
      <!-- movieList를 평점순, 조회순으로 받기 위한 computed 입니다. 있어야합니다. -->
      {{ view_by_averagerate }}
      <!-- 처음에 보여주는 것 : 조회수 순 -->
      <v-flex v-if="!seemode_rate" v-for="(card,i) in movieListCardsSliced" :key="i" xs12 sm6 md4 lg3 xl2 style="height: 22rem; width: 28rem;">
        <MovieListCard
          :id="card.id"
          :title="card.title"
          :genresarray="card.genres_array"
          :averagerate="card.averagerate"
          :watchcount="card.watch_count"
          :scoreusers="card.score_users"
          :plot="card.plot"
          :url="card.url"
          :director="card.director"
          :casting="card.casting"
        />
      </v-flex>

      <!-- 선택옵션 - 평점 순 -->
      <v-flex v-if="seemode_rate" v-for="(card, i) in movieListCardsSliced2" :key="i" xs12 sm6 md4 lg3 xl2 style="height: 22rem; width: 28rem;">
        <MovieListCard
          :id="card.id"
          :title="card.title"
          :genresarray="card.genres_array"
          :averagerate="card.averagerate"
          :watchcount="card.watch_count"
          :scoreusers="card.score_users"
          :plot="card.plot"
          :url="card.url"
          :director="card.director"
          :casting="card.casting"
        />
      </v-flex>
      <v-flex v-if="page==maxPages && $store.state.data.canmore==true" xs12 sm6 md4 lg3 xl2 style="height: 22rem; width: 28rem;">
        <v-btn fab style="margin-top: 1.5rem; margin-bottom: 2rem;" @click="before_plusMovies()"><v-icon dark>mdi-plus</v-icon></v-btn>
      </v-flex>
      <v-pagination v-if="maxPages > 1" v-model="page" :length="maxPages" />
    </v-layout>
  </v-container>
</template>

<script>
import MovieListCard from "./MovieListCard"
import { mapActions } from "vuex";

export default {
  components: {
    MovieListCard,
  },
  props: {
    movieListCards: {
      type: Array,
      default: () => new Array(),
    },
    reset : {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    cardsPerPage: 12,
    page: 1,
    seemode_rate:false,
    tmp_movieList:[],
    // movielist:[],
    num:1,
  }),
  computed: {
    // pagination related variables
    movieListEmpty: function() {
      return this.$store.state.data.movieSearchList.length === 0;
    },
    maxPages: function() {
      return Math.floor((this.$store.state.data.movieSearchList.length + this.cardsPerPage - 1) / this.cardsPerPage)
    },
    movieListCardsSliced: function() {
      this.tmp_movieList = JSON.parse(JSON.stringify(this.movieListCards))
      return this.movieListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
    },
    movieListCardsSliced2: function() {
      return this.tmp_movieList.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
    },
    view_by_averagerate: function() {
      // 참조 사이트 : https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
      this.tmp_movieList.sort(function(a, b) {
        if (a.averagerate > b.averagerate) {
          return -1;
        }
        if (a.averagerate < b.averagerate) {
          return 1;
        }
        return 0;
      })
    },
  },
  watch: {
    reset: function () {
      this.page = 1
    },
  },
  methods: {
    ...mapActions("data", ["plusMovies"]),
    before_plusMovies() {
      this.plusMovies({'title':this.$store.state.data.recent_SearchName, 'num':this.num})
      this.num += 1
    },
  }
};
</script>
