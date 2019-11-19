<template>
  <v-container grid-list-md text-center style="width: 60rem;">
    <SignUpForm />
  </v-container>
</template>

<script>
import SignUpForm from "../SignUpForm";
import router from "../../router";

export default {
  components: {
      SignUpForm
  },
  created() {
    if (this.$session.get('id')!='') {
      this.$swal.fire({
          type: 'error',
          title: 'Oops...',
          text: '이미 로그인한 상태입니다!',
        })
      router.push({name:"home"})
    }
  },
};
</script>
