<template>
  <v-form ref="form">
    <div>
      <br>
      <div v-for="(occupation, index) in occupations" :key="index" style="display:inline-block;">
        <input v-model="picked" type="radio" :value="occupation">
        <label style="font-size:10px;">{{ occupation }}</label> &nbsp;
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
    occupations : ['전체보기','academic/educator', 'artist', 'clerical/admin', 'college/grad student', 'customer service', 'doctor/health care', 'executive/managerial',
                  'farmer', "homemaker", "K-12 student", "lawyer", "programmer", "retired", "sales/marketing", "scientist", "self-employed", "technician/engineer",
                  "tradesman/craftsman", "unemployed", "writer"],
    picked:'',
  }),
  methods: {
    onSubmit: function() {
      if (this.picked == '전체보기') {
        const params = {
          occupation: '',
        };
        this.submit(params);
      } else {
        // console.log(this.picked, 123123)
        const params = {
          occupation: this.picked,
        };
        this.submit(params);
      }

    },

  }
};
</script>
