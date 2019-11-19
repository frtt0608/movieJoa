<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 by 영화이름-->
      <v-flex>
        <div style="color:rgb(255,255,255)">No. {{ profile_data[0].id }}</div>
        <v-card class="mx-auto" max-width="600px" color="#424242" dark>
          <v-col>
            <h1>{{ profile_data[0].username }}</h1>
            <div v-if="profile_data[0]['gender'] == 'F'" class="grey--text">Gender: 여</div>
            <div v-else-if="profile_data[0]['gender'] == 'M'" class="grey--text">Gender: 남</div>
            <div class="grey--text">Occupation: {{ profile_data[0]['occupation'] }}</div>
            <div v-if="profile_data[0]['age'] == '1'" class="grey--text">Age: 18세이하</div>
            <div v-else-if="profile_data[0]['age'] == '18'" class="grey--text">Age: 18-24세</div>
            <div v-else-if="profile_data[0]['age'] == '25'" class="grey--text">Age: 25-34세</div>
            <div v-else-if="profile_data[0]['age'] == '35'" class="grey--text">Age: 35-44세</div>
            <div v-else-if="profile_data[0]['age'] == '45'" class="grey--text">Age: 45-49세</div>
            <div v-else-if="profile_data[0]['age'] == '50'" class="grey--text">Age: 50-55세</div>
            <div v-else-if="profile_data[0]['age'] == '56'" class="grey--text">Age: 56세이상</div>
          </v-col>
        </v-card>
        <p style="font-size: 3rem; color: white; font-family: 'Jua', sans-serif;">Similar Users</p>
      </v-flex>
      <v-layout v-if="profile_data.length > 1" pa-5>
        <v-flex>
          <carousel :per-page="3">
            <slide v-for="(person, index) in profile_data.slice(1,6)" :key="index" style="height: 6rem; width: 15rem;">
              <v-card style="margin:10px; height: 5rem; width: 20rem; border-radius:15px;" color="#424242" dark>
                <v-card-text>
                  <div>{{ person.id }} | {{ person.username }}</div>
                  <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_UserDetail(person.id, person.username)">explore</v-btn>
                </v-card-text>
              </v-card>
            </slide>
          </carousel>
        </v-flex>
      </v-layout>
      <v-btn @click="search()">검색으로 이동</v-btn>
    </v-layout>
  </v-container>
</template>

<script>
import router from "../../router";
import axios from 'axios'
import { Carousel, Slide } from 'vue-carousel'

export default {
  components: {
    Carousel,
    Slide
  },
  props: {
    id : {
      type: [Number, String],
      default: () => {}
    },
  },
  data: () => ({
    profile_data:[
      {'id':''},
      {"approval":''},
      {"gender":''},
      {"age":''},
      {"is_staff":''},
      {"occupation":''},
      {"subscription":''},
      {"username":''}],
  }),
  mounted() {
    this.fetchdata()
  },
  methods: {
    async fetchdata() {
      const apiUrl = '/api'
      const id = this.$route.params.id
      var profile = await axios.get(`${apiUrl}/users/${id}`)
      this.profile_data = profile.data
      // console.log(profile)
    },
    search() {
      router.push({name:'user-search'})
    },

    SELECT_UserDetail(id, username) {
      var user_data = {'id':id, 'username':username}
      router.push({name:'user-detail', params : {'id':user_data.id, 'user_data':user_data}})
      window.location.reload()
    }

  }
};
</script>
