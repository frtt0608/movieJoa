<template>
  <v-form ref="form">
    <div>
      <br>
      <div v-for="(genre, i) in genres" :key="i" style="display:inline-block;">
        <input v-model="picked" type="radio" :value="genre">
        <label style="font-size:10px;">{{ genre }}</label> &nbsp;
      </div>
    </div>
    <br>
    <v-btn large color="indigo white--text" @click="onSubmit">Search</v-btn>
  </v-form>
</template>

<script>
export default {
  props: {
    submit: {
      type: Function,
      default: () => {}
    }
  },
  data: () => ({
    title: "",
    genres : ['전체보기','Action', 'Adventure', 'Animation', "Children's", 
              'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 
              'Sci-Fi', 'Thriller', 'War', 'Western'],
    picked:'',
  }),
  methods: {
    onSubmit: function() {
      if (this.picked == '전체보기') {
        const params = {
          genre: '',
        };
        this.submit(params);
      } else {
        const params = {
          genre: this.picked,
        };
        this.submit(params);
      }

    },

  }
};
</script>
