<template>
  <v-form ref="form">
    <v-text-field v-model="username" dark label="유저 이름" @keyup.enter="onSubmit" />

    <!-- enter 치면 리렌더링 방지용 -->
    <v-text-field v-show="false" />

    <v-layout justify-center pa-10>
      <v-btn large color="indigo white--text" @click="onSubmit">Search</v-btn>
    </v-layout>
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
    username: ""
  }),
  methods: {
    onSubmit: function() {
      const params = {
        username: this.username,
      };
      this.submit(params);
    }
  }
};
</script>
