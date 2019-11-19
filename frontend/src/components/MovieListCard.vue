<template>
  <v-layout row wrap text-left>
    <v-flex>
      <v-card style="margin:10px; height: 21rem; width: 15rem; border-radius:15px;" color="#424242" dark>
        <v-img :src="url || 'https://cdn.samsung.com/etc/designs/smg/global/imgs/support/cont/NO_IMG_600x600.png'" style="height:16rem; width: 15rem;" />
        <v-card-text>
          <div class="movietitle">
            {{ title.substring(0, title.indexOf("(")) }}<br>
            <span class="hovertext2">{{ title.substring(0) }}</span>
          </div>
          <i class="fas fa-star" style="color: #FFB600;" /><span>평점 </span><span style="font-weight: bold;">{{ Math.round(averagerate*100)/100 }}</span>
          <span><v-btn text color="primary" @click="SELECT_MovieDetail()">explore</v-btn></span>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import router from "../router";

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
  computed: {
    genresStr: function() {
      if (typeof(this.genres_array)=="object") {
        return this.genres_array.join(" / ");
      } else {
        return this.genres_array.split('|').join(" / ");
      }
    },
  },
  methods: {
    SELECT_MovieDetail() {
      var movie_data = {'id':this.id, 'title':this.title, 'genres_array':this.genres_array,
                  'watch_count' : this.watch_count, 'score_users':this.score_users, 'averagerate':this.averagerate,
                  'plot':this.plot,'url':this.url,'director':this.director,'casting':this.casting}
      router.push({name:'movie-detail', params : {'id':movie_data.id}})
    }
  }
};
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
