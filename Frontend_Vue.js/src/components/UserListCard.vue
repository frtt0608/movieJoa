<template>
  <v-hover v-slot:default="{ hover }">
    <v-card :elevation="hover ? 8 : 2" style="margin:10px; height: 5rem; width: 20rem; border-radius:15px;" color="#424242" dark>
      <v-card-text>
        <div>{{ id }} | {{ username }}</div>
        <v-btn text color="primary" style="padding-right: 0; margin-left: 2rem; margin-right: 0;" @click="SELECT_UserDetail()">explore</v-btn>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script>
import router from "../router";

export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    username: {
      type: String,
      default : ''
    }
  },
  methods: {
    SELECT_UserDetail() {
      var user_data = {'id':this.id, 'username':this.username}
      router.push({name:'user-detail', params : {'id':user_data.id, 'user_data':user_data}})
    }
  }

};
</script>
