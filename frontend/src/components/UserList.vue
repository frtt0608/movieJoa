<template>
  <v-container class="pa-2" fluid grid-list-md>
    <div v-if="userListCards.length" style="color: white">
      {{ userListCards.length }}명이 조회되었습니다.
    </div>

    <!-- <div v-if="!userListCards.length" style="color: white">
      검색하신 유저가 없습니다!
    </div> -->

    <v-layout row wrap>
      <!-- {{userListCards}} -->
      <v-flex v-for="(card, i) in userListCardsSliced" :key="i" pa-2 xs12 sm6 md4 lg3 xl2>
        <UserListCard
          :id="card.user_id"
          :username="card.username"
        />
      </v-flex>
      <v-pagination v-if="maxPages > 1" v-model="page" :length="maxPages" />
    </v-layout>
  </v-container>
</template>

<script>
import UserListCard from "./UserListCard"
export default {
  components: {
    UserListCard
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
      return this.userListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
    },
  },
};
</script>