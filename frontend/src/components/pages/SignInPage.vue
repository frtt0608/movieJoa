<template>
  <v-container grid-list-md text-center style="width: 50rem;" @keyup.enter="login">
    <v-card wdith="width" color="#424242" dark>
      <v-card-text>
        <p style="text-align: center; font-size: 2.5rem; padding-bottom: 3rem; padding-top: 3rem;">Sign in</p>
        <form>
          <v-text-field
            v-model="username"
            :counter="10"
            label="Name"
            :rules="nameRules"
            required
            style="margin-left: 5rem; margin-right: 5rem;"
          />
          <v-text-field
            v-model="password"
            label="Password"
            :counter="20"
            :rules="passwordRules"
            type="password"
            required
            style="margin-left: 5rem; margin-right: 5rem;"
          />
          <v-btn style="margin-top: 2rem; margin-bottom: 1rem;" @click="login">Sign in</v-btn>
        </form>
        <div style="padding-top: 1.5rem; padding-bottom: 3rem;">
          <router-link to="signup">아직 회원이 아니신가요?</router-link>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import router from "../../router";
import axios from 'axios'

export default {
  components: {
  },
  data() {
    return {
      username: '',
      password: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 10) || 'Name must be less than 10 characters'
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 5 && v.length <= 20) || 'Password must be 5~20 characters'
      ],
    }
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
  methods: {
    async login() {
      const apiUrl = '/api'
      let __this = this
      await axios.post(`${apiUrl}/auth/signin/`, {
        username: __this.username,
        password: __this.password
      }).then(async res => {
        if (res.data.user != '') {
          this.$store.commit('data/setUser', __this.username)
          this.$session.set('id', res.data.user)
          this.$session.set('id_number', res.data.id_number)
          this.$session.set('admin', res.data.admin)
          var profile = await axios.get(`/api/users/${res.data.id_number}`)
          const flag = typeof(profile.data[1])
          this.$swal.fire({
            title: '로그인 완료!',
            type: 'success'
          }).then(() => {
            if (flag != 'boolean' || res.data.id_number < 6042) {
              router.push('/')
              window.location.reload()
            } else {
              router.push('/choices/')
              window.location.reload()
            }
          })
        }
         else {
          __this.username = ''
          __this.password = ''
          // alert('ID 또는 비밀번호가 다릅니다. 확인해주세요!')
          this.$swal.fire({
            text: 'ID 또는 비밀번호가 다릅니다. 확인해주세요!',
            type: 'error'
          })
        }
      })
    },
    // async usercheck() {
    //   let tmp = await axios.get('/api/auth/userState').then(res => {
    //     if (res.data.user != '') {
    //       router.go(-1)
    //     }
    //   })
    // }
  }
};
</script>
