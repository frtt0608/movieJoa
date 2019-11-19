<template>
  <v-card color="#424242" dark>
    <v-card-text>
      <p style="text-align: center; font-size: 2.5rem; padding-bottom: 3rem; padding-top: 3rem;">Sign up</p>
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
          style="margin-left: 5rem; margin-right: 5rem;"
          required 
        />
        <v-layout style="margin-left: 5rem; margin-right: 5rem;">
          <span style="vertical-align: middle; color: rgba(0, 0, 0, 0.54); padding-left: 0.3rem; padding-right: 2.5rem;">Gender</span>
          <v-radio-group v-model="gender" row>
            <v-radio label="Female" value="F" />
            <v-radio label="Male" value="M" />
          </v-radio-group>
        </v-layout>
        <v-text-field
          v-model="age"
          type="number"
          label="Age"
          :rules="ageRules"
          style="margin-left: 5rem; margin-right: 5rem;"
          required 
        />
        <v-select
          v-model="occupation"
          :items="occupations"
          label="Occupation"
          :rules="occupationRules"
          style="margin-left: 5rem; margin-right: 5rem;"
          required 
        />
        <v-btn v-if="nameRules[0](username)===true && passwordRules[0](password)===true && ageRules[0](age)===true && occupationRules[0](occupation)===true" style="margin-top: 2rem; margin-bottom: 1rem;" @click="submit">Sign up</v-btn>
        <v-btn v-else disabled style="margin-top: 2rem; margin-bottom: 1rem;">Sign up</v-btn>
      </form>
      <div style="padding-top: 1.3rem; padding-bottom: 3rem;">
        <router-link to="signin">계정이 있으신가요?</router-link>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  components: {
  },
  data() {
    return {
      username: '',
      password: '',
      gender: 'F',
      age: null,
      occupations: ["other","academic/educator","artist","clerical/admin","college/grad student",
      "customer service","doctor/health care","executive/managerial","farmer","homemaker",
      "K-12 student","lawyer","programmer","retired","sales/marketing","scientist",
      "self-employed","technician/engineer","tradesman/craftsman","unemployed","writer"],
      occupation: '',
      nameRules: [
        function(v) {
          // 아예 없는지 체크
          if (!v) {
            return 'Name is required'
          }
          // 길이 제한 체크
          if (v.length > 10) {
            return 'Name must be less than 10 characters'
          }
          // 공백 체크
          if (v!==v.replace(/(\s*)/g,"")) {
            return "공백은 안돼요~"
          }
          //특수문자 체크
          var pattern_spc = /[~!@#$%^&*()_+|<>?:{}]/;
          if (pattern_spc.test(v)) {
            return "username에 특수문자는 사용 불가능!"
          }
          return !!v
        },
      ],
      passwordRules: [
        function(v) {
          // 아예 없는지 체크
          if (!v) {
            return 'Password is required'
          }
          // 길이 제한 체크
          if (v.length < 5 || v.length > 20) {
            return 'Password must be 5~20 characters'
          }
          // 공백 체크
          if (v!==v.replace(/(\s*)/g,"")) {
            return "공백은 안돼요~"
          }
          return !!v
        },
      ],
      ageRules : [
        function(v) {
          // 양수인지 체크
          if (v<=0) {
            return 'Age must be more than 1'
          } return !!v
        }
      ],
      occupationRules : [
        function(v) {
          // 등록했는지 체크
          if (!v) {
            return 'Occupation is required'
          } return !!v
        }
      ]
    }
  },
  watch: {
  },
  methods: {
    async submit() {
      const apiUrl = '/api'
      let __this = this;
      await axios.post(`${apiUrl}/auth/signup/`, {
        username: __this.username,
        password: __this.password,
        gender: __this.gender,
        age: __this.age,
        occupation: __this.occupation
      }).then(res => {
        if (res.data == true) {
          this.$swal.fire({
            title:'회원가입 성공!',
            type: 'success'
          })
          this.$router.push('/users/signin');
        } else {
          this.$swal.fire({
            title:'중복된 name입니다!',
            type: 'error'
          })
        }
      })
    },
  }
};
</script>