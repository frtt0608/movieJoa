<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">Admin page</p>
      <v-flex fluid row justify-center style="width:100%;">
        <v-switch v-model="switch1" :label="`movie`" dark @click="one()" />
        <v-switch v-model="switch2" :label="`user`" dark @click="two()" />
        <v-switch v-model="switch3" :label="`clustering`" dark @click="three()" />
        <v-switch v-model="switch4" :label="`subscription`" dark @click="four()" />
      </v-flex>
      <v-flex xs12>
        <v-btn @click="check()">초기화</v-btn>
      </v-flex>
      <v-flex v-if="switch1" xs12 wrap>
        <div class="display-2 pa-10" style="color:white">영화 검색</div>
        <v-flex xs6 offset-3>
          <v-btn v-if="!create" @click="createMovie()">create</v-btn>
          <v-btn v-if="create" @click="createMovie()">cancel</v-btn>
          <CreateMovieForm v-if="create" />
          <MovieSearchForm v-if="!create" :submit="before_searchMovies" />
        </v-flex>
        <v-flex xs12>
          <AdminMovieList :movie-list-cards="movieList" />
        </v-flex>
      </v-flex>
      <v-flex v-if="switch2" xs12>
        <div class="display-2 pa-10" style="color:white">유저 검색</div>
        <v-flex xs6 offset-3>
          <UserSearchForm :submit="before_searchUsers" />
        </v-flex>
        <v-flex xs12>
          <AdminUserList :user-list-cards="userList" />
        </v-flex>
      </v-flex>
      <v-flex v-if="switch3" xs8>
        <v-card color="#424242" dark>
          <p style="font-size: 3rem; font-family: 'Jua', sans-serif; color:black">Clustering 파라미터 설정하기</p>
          <AdminClustering />
        </v-card>
      </v-flex>
      <v-flex v-if="switch4" xs12>
        <p style="font-size: 3rem; font-family: 'Jua', sans-serif; color:black">구독자들의 신청목록 관리</p>
        <AdminSubscriptionList />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import MovieSearchForm from "../searchform/MovieSearchForm";
import AdminMovieList from "../AdminMovieList";
import UserSearchForm from "../searchform/UserSearchForm";
import AdminUserList from "../AdminUserList";
import AdminClustering from "../AdminClustering";
import AdminSubscriptionList from "../AdminSubscriptionList";
import CreateMovieForm from "../CreateMovieForm";
import router from "../../router";

export default {
  components: {
    AdminMovieList,
    AdminUserList,
    AdminSubscriptionList,
    MovieSearchForm,
    UserSearchForm,
    AdminClustering,
    CreateMovieForm,
  },
  data: () => ({
    switch1: false,
    switch2: false,
    switch3: false,
    switch4: false,
    movielist:[],
    userlist:[],
    create: false,
  }),
  computed: {
    ...mapState({
      movieList: state => state.data.movieSearchList_admin,
      userList: state => state.data.userSearchList_admin
    })
  },
  created() {
    if (this.$session.get('admin')!=true) {
      this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '관리자 권한이 없습니다!',
        })
      router.push({name:"home"})
    }
  },
  methods: {
    ...mapActions("data", ["searchMovies_admin", "searchUsers_admin"]),
    async before_searchMovies(params) {
      this.reset = !this.reset
      var result = await this.searchMovies_admin(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    async before_searchUsers(params) {
      this.reset = !this.reset
      var result = await this.searchUsers_admin(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 영화는 없습니다!',
        })
      }
    },
    one() {
      this.switch1 = true
      this.switch2 = false
      this.switch3 = false
      this.switch4 = false
    },
    two() {
      this.switch1 = false
      this.switch2 = true
      this.switch3 = false
      this.switch4 = false
    },
    three() {
      this.switch1 = false
      this.switch2 = false
      this.switch3 = true
      this.switch4 = false
    },
    four() {
      this.switch1 = false
      this.switch2 = false
      this.switch3 = false
      this.switch4 = true
    },
    check() {
      this.switch1 = false
      this.switch2 = false
      this.switch3 = false
      this.switch4 = false
    },
    createMovie() {
      this.create = !(this.create);
    }
  }
}
</script>
