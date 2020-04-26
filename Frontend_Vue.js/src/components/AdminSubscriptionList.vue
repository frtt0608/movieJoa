<template>
  <v-container class="pa-2" fluid grid-list-md>
    <v-layout column>
      <v-flex>
        <div v-for="(subscription, index) in subscriptions" :key="index">
          <v-icon dark>mdi-account</v-icon>
          <span v-if="subscription.approval==false" style="font-size: 1rem; font-family: 'Jua', sans-serif; color:white">
            <strong style="font-size: 2rem;">{{ subscription.username }}</strong>님이 
            <strong style="font-size: 2rem;">{{ subscription.request }}</strong>일 구독 신청하였습니다.</span><br>
          <v-btn @click="approval(subscription, index)">승인</v-btn>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data: () => ({
    subscriptions : []
  }),
  mounted() {
    this.fecthdata()
  },
  methods : {
    async fecthdata() {
      const apiUrl = '/api'
      var sub = await axios.get(`${apiUrl}/subscription/manager/`)
      this.subscriptions = sub.data
    },
    async approval(subscription, index) {
      const apiUrl = '/api'
      this.subscriptions.splice(index, 1)
      axios.post(`${apiUrl}/subscription/manager/`, {subscription : subscription})
    }
  }

};
</script>
