<template>
  <v-form ref="form">
    <div>
      <br>
      <div v-for="(gender, index) in genders" :key="index" style="display:inline-block;">
        <input v-model="picked" type="radio" :value="gender">
        <label style="font-size:10px;">{{ gender }}</label> &nbsp;
      </div>
    </div>
    <br>
    <v-btn large color="indigo white--text" @click="onSubmit">Search</v-btn>
    <!-- 	M, F -->
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
    genders : ['전체보기','M', 'F'],
    picked:'',
  }),
  methods: {
    onSubmit: function() {
      if (this.picked == '전체보기') {
        const params = {
          gender: '',
        };
        this.submit(params);
      } else {
        const params = {
          gender: this.picked,
        };
        this.submit(params);
      }

    },

  }
};
</script>
