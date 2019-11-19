<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 by username-->
      <v-flex xs6>
        <div class="display-2 pa-10" style="color: white">유저 검색</div>
        <UserSearchForm :submit="before_searchUsers" />
      </v-flex>
      <!-- 검색 결과 -->
      <v-flex xs12>
        <UserList :user-list-cards="userList" />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import UserSearchForm from "../searchform/UserSearchForm";
import UserList from "../UserList";
export default {
  components: {
    UserList,
    UserSearchForm,
  },
  data: () => ({
    userlist:[],
  }),
  computed: {
    ...mapState({
      userList: state => state.data.userSearchList
    })
  },
  methods: {
    ...mapActions("data", ["searchUsers"]),
    async before_searchUsers(params) {
      this.reset = !this.reset
      var result = await this.searchUsers(params)
      if (result.length === 0) {
        this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '해당 이름의 유저는 없습니다!',
        })
      }
    },
  }
};
</script>
