<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <div>
      <p style="color: white; font-size: 1.4rem; font-family: 'Jua', sans-serif;">10개 이상 평점을 매겨주세요. 더 많이 평점을 줄수록 정확한 추천을 드립니다 :)</p>
      <v-btn color="red lighten-2" dark style="margin-bottom: 1rem;" @click="save()">평가 완료</v-btn>
    </div>
    <v-layout justify-center wrap>
      <!-- 처음에 보여주는 것 : 조회수 순 -->
      <v-flex v-for="(card,i) in movielist" :key="i" xs12 sm6 md4 lg3 xl2 style="height: 26rem; width: 28rem;">
        <v-card style="margin:10px; height: 25rem; width: 15rem; border-radius:15px;" color="#424242" dark>
          <v-img :src="card.url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
          <v-card-text>
            <!-- <p style="font-size: 1rem;">{{ card.title }}</p> -->
            <p class="movietitle" style="font-size: 1rem; -webkit-transition: 0.5;">
              {{ card.title.substring(0, card.title.indexOf("(")) }}<br>
              <span class="hovertext2">{{ card.title.substring(0) }}</span>
            </p>
            <div class="text-center mt-1" @click="plus(card.id, card.rating)">
              <v-rating
                v-model="card.rating"
                color="yellow darken-3"
                background-color="grey darken-1"
                half-increments
                hover
              />
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-btn fab style="margin-top: 1.5rem; margin-bottom: 2rem;" @click="before_plusMovies()"><v-icon dark>mdi-plus</v-icon></v-btn>
    <v-btn href="#" style="margin-top: 1.5rem; margin-bottom: 2rem; position:fixed; bottom:0%; right:1%;" fab><v-icon dark>mdi-chevron-double-up</v-icon></v-btn>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import axios from 'axios';
import router from "../../router";

export default {
  data: () => ({
    movielist:[],
    bymoviename:true,
    bygenre:false,
    byage:false,
    byoccupation:false,
    bygender:false,
    reset : true,
    num:1,
    rating: 0,
    rating_box:{}
  }),
  mounted() {
      this.onSubmit();
  },
  methods: {
    ...mapActions("data", ["searchMovies", "plusMovies"]),
    onSubmit: function() {
        const apiUrl = '/api'
        const params = {
            title: ''
        }
        axios.get(`${apiUrl}/movies`, {
            params
        }).then(res => {
            let tmp = []
            res.data[0].forEach(ele => {
                ele['rating'] = 0
                tmp.push(ele)
            })
            this.movielist = tmp
        })
    },
    before_plusMovies() {
      const params = {'title':'', 'num':this.num}
      const apiUrl = '/api'
      this.num += 1
      axios.get(`${apiUrl}/movies`, {
            params
        }).then(res => {
            let tmp = []
            res.data[0].forEach(ele => {
                ele['rating'] = 0
                tmp.push(ele)
            })
            this.movielist = this.movielist.concat(res.data[0])
        })
    },
    save() {
      if (Object.keys(this.rating_box).length >= 10) {
        const apiUrl = '/api'
        axios.post(`${apiUrl}/signup/new_cluster/`, {
            user_pk:this.$session.get("id_number"),
            movies:this.rating_box,
        }).then(res => {
            if(res.data==2) {
                this.$swal.fire({
                    title: '평점등록 성공!',
                    type: 'success'
                })
                .then(() => {
                  router.push({name:"home"})
                  window.location.reload()
                })
            } else if(res.data==1) {
                this.$swal.fire({
                    title: '이미 평점등록을 하셨습니다!',
                    type: 'error'
                })
                router.push({name:"home"})
            } else if(res.data==0) {
              this.$swal.fire({
                    title: '로그인부터 해주세요!',
                    type: 'error'
                })
                router.push({name:"home"})
            }
        })
      } else {
        this.$swal.fire({
          title:'10개 이상 해주세요',
          text: `현재까지 평가한 영화갯수 : ${Object.keys(this.rating_box).length}개`,
          type: 'error'
        })
      }
    },
    plus(id, rating) {
      this.rating_box[id]=rating
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
