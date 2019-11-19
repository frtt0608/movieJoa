<template>
  <div>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model="title"
        :counter="30"
        label="Title"
        :rules="titleRules"
        required
        dark
      />
      <v-select
        v-model="genres"
        :items="items"
        label="Genre"
        :rules="genresRules"
        multiple
        required
        dark
      />
      <v-text-field
        v-model="url"
        label="ImageURL"
        :rules="urlRules"
        required
        dark
      />
      <v-text-field
        v-model="director"
        label="Director"
        :rules="directorRules"
        required
        dark
      />
      <v-combobox
        v-model="casting"
        label="Casting"
        :rules="castingRules"
        hint="Maximum of 5 tags"
        persistent-hint
        small-chips
        multiple
        required
        dark
      />
      <v-textarea
        v-model="plot"
        solo
        :counter="500"
        label="Plot"
        :rules="plotRules"
        required
      />
      <!-- <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">Validate</v-btn> -->
      <v-btn color="error" class="mr-4" @click="reset">Reset Form</v-btn>
    </v-form>
    <v-dialog v-model="dialog" persistent max-width="700">
      <template v-slot:activator="{ on }">
        <v-btn v-if="titleRules[0](title)===true && genresRules[0](genres)===true && urlRules[0](url)===true && directorRules[0](director)===true && castingRules[0](casting)===true && plotRules[0](plot)===true" color="success" class="mr-4" dark v-on="on">영화 등록하기</v-btn>
        <v-btn v-else disabled color="dark" class="mr-4" dark v-on="on">모든 data를 채워주세요!</v-btn>
      </template>
      <v-card>
        <v-card-title class="headline">{{ title }}</v-card-title>
        <v-card-text>장르: {{ genres }}</v-card-text>
        <v-card-text>이미지url: {{ url }}</v-card-text>
        <v-card-text>감독: {{ director }}</v-card-text>
        <v-card-text>배우: {{ casting }}</v-card-text>
        <v-card-text>줄거리: {{ plot }}</v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="createMovie();dialog=false">OK</v-btn>
          <v-btn color="green darken-1" text @click="dialog=false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  components: {

  },
  data: () => ({
    valid: true,
    dialog: false,
    title:'',
    genres:[],
    plot:'',
    url:'',
    director:'',
    casting:[],
    items: ['Action', 'Adventure', 'Animation', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', "Children's"],
    titleRules: [
      v => !!v || 'This is required',
      v => (v && v.length <= 30) || 'Name must be less than 30 characters',
    ],
    genresRules : [
      function(v) {
        if (v.length===0) {
          return 'Genre is required'
        }
        return !!v
      }
    ],
    urlRules : [
      function(v) {
        if (!v) {
          return 'Url is required'
        }
        return !!v
      }
    ],
    directorRules : [
      function(v) {
        if (!v) {
          return 'Director is required'
        }
        return !!v
      }
    ],
    castingRules : [
      function(v) {
        if (v.length===0) {
          return 'Casting is required'
        }
        return !!v
      }
    ],
    plotRules : [
      function(v) {
        if (!v) {
          return 'Plot is required'
        }
        return !!v
      }
    ],
  }),
  watch: {
    casting (val) {
      if (val.length > 5) {
        this.$nextTick(() => this.casting.pop())
      }
    },
  },
  methods: {
    validate () {
      if (this.$refs.form.validate()) {
        this.snackbar = true
      }
    },
    reset () {
      this.$refs.form.reset()
    },
    createMovie: function() {
      const apiUrl = '/api'
      var preload = document.querySelector('#check1')
      preload.style.display = 'block'

      axios.post(`${apiUrl}/KNN/movie/`, {
        title:this.title,
        genres:this.genres,
        plot:this.plot,
        url:this.url,
        director:this.director,
        casting:this.casting
      }).then(() => {
        preload.style.display = 'none'
        this.$swal.fire ({
          type: 'success',
          title: '영화가 등록되었습니다!'
        }).then(result => {
          this.$refs.form.reset()
        })
      })
    }
  }
}
</script>
