<template>
  <v-container class="pa-2" fluid grid-list-md>
    <v-layout row wrap>
      <v-flex v-for="(card, i) in userListCardsSliced" :key="i" pa-2 xs12 sm6 md4 lg3 xl2>
        <AdminUserListCard
          :id="card.user_id"
          :username="card.username"
        />
      </v-flex>
      <v-pagination v-if="maxPages > 1" v-model="page" :length="maxPages" />
    </v-layout>
  </v-container>
</template>

<script>
import AdminUserListCard from "./AdminUserListCard"

export default {
  components: {
    AdminUserListCard
  },
  props: {
    userListCards: {
      type: Array,
      default: () => new Array(),
    },
  },
  data: () => ({
    cardsPerPage: 12,
    page: 1,
  }),
  computed: {
    // pagination related variables
    userListEmpty: function() {
      return this.userListCards.length === 0;
    },
    maxPages: function() {
      // 이전에 검색한 다음 page가 1이 아닌 경우, 새로운 검색을 하면 page를 초기화 해주어야 한다.
      this.page = 1
      return Math.floor((this.userListCards.length + this.cardsPerPage - 1) / this.cardsPerPage)
    },
    userListCardsSliced: function() {
      // console.log(this.userListCards, 3)
      return this.userListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
    },
  }
};
</script>
