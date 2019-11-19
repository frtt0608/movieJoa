<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 by 영화이름-->
      <v-flex v-if="bymoviename" xs6>
        <div class="display-2 pa-10" style="color: white">영화 검색</div>
        <v-btn @click="changesearch1()">다른 검색</v-btn>
        <div>
          <MovieSearchForm :submit="before_searchMovies" />
        </div>
      </v-flex>

      <!-- 검색 폼 by 장르이름 -->
      <v-flex v-if="!bymoviename" xs6>
        <v-btn @click="changesearch1()">영화 이름으로 검색하기</v-btn><br>
        <v-btn @click="changesearch2()">장르 기준</v-btn>
        <v-btn @click="changesearch3()">연령대 기준</v-btn>
        <v-btn @click="changesearch4()">직업 기준</v-btn>
        <v-btn @click="changesearch5()">성별 기준</v-btn>

        <div v-if="bygenre" class="display-2 pa-10" style="color: white">장르 검색<GenreSearchForm :submit="before_searchGenres" /></div>
        <div v-if="byage" class="display-2 pa-10" style="color: white">연령대 검색<AgeSearchForm :submit="before_searchAges" /></div>
        <div v-if="byoccupation" class="display-2 pa-10" style="color: white">직업 검색<OccupationSearchForm :submit="before_searchOccupations" /></div>
        <div v-if="bygender" class="display-2 pa-10" style="color: white">성별 검색<GenderSearchForm :submit="before_searchGenders" /></div>
      </v-flex>

      <!-- 검색 결과 -->
      <v-flex xs12>
        <MovieList :movie-list-cards="movieList" :reset="reset" />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import MovieSearchForm from "../searchform/MovieSearchForm";
import GenreSearchForm from "../searchform/GenreSearchForm";
import AgeSearchForm from "../searchform/AgeSearchForm";
import OccupationSearchForm from "../searchform/OccupationSearchForm";
import GenderSearchForm from "../searchform/GenderSearchForm";
import MovieList from "../MovieList";
export default {
  components: {
    MovieList,
    MovieSearchForm,
    GenreSearchForm,
    AgeSearchForm,
    OccupationSearchForm,
    GenderSearchForm
  },
  data: () => ({
    movielist:[],
    bymoviename:true,
    bygenre:false,
    byage:false,
    byoccupation:false,
    bygender:false,
    reset : true,
  }),
  computed: {
    ...mapState({
      movieList: state => state.data.movieSearchList
    })
  },
  methods: {
    ...mapActions("data", ["searchMovies", "searchGenres", "searchAges", "searchOccupations", "searchGenders", "resetMovieList"]),
    async before_searchMovies(params) {
      this.reset = !this.reset
      var result = await this.searchMovies(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    async before_searchGenres(params) {
      this.reset = !this.reset
      var result = await this.searchGenres(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    async before_searchAges(params) {
      this.reset = !this.reset
      var result = await this.searchAges(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    async before_searchOccupations(params) {
      this.reset = !this.reset
      var result = await this.searchOccupations(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    async before_searchGenders(params) {
      this.reset = !this.reset
      var result = await this.searchGenders(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    changesearch1() {
      this.bymoviename = !this.bymoviename
      this.bygenre = false
      this.byage = false
      this.byoccupation = false
      this.bygender = false
    },
    changesearch2() {
      // 장르별 하기 위함
      this.bygenre = true
      this.byage = false
      this.byoccupation = false
      this.bygender = false
    },
    changesearch3() {
      // 나이별 하기 위함
      this.bygenre = false
      this.byage = true
      this.byoccupation = false
      this.bygender = false
    },
    changesearch4() {
      // 직업별 하기 위함
      this.bygenre = false
      this.byage = false
      this.byoccupation = true
      this.bygender = false
    },
    changesearch5() {
      // 나이별 하기 위함
      this.bygenre = false
      this.byage = false
      this.byoccupation = false
      this.bygender = true
    },
  }
};
</script>
