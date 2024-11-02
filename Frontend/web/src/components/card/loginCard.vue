<template>
    <baseCard title="Login" cardClass="login-card">
      <form @submit.prevent="handleLogin">
        <label>
          Email:
          <input type="text" v-model="email" />
        </label>
        <label>
          Password:
          <input type="password" v-model="password" />
        </label>
        <button type="submit">Login</button>
      </form>
    </baseCard>
  </template>
  
  <script>
  import baseCard from '../base/baseCard.vue';
  
  export default {
    name: "CardLoginComponent",
    components: {
        baseCard
    },
    data() {
      return {
        email: "",
        password: ""
      };
    },
    methods: {
      handleLogin() {
        // Logic untuk login
        console.log("Login dengan:", this.username, this.password);
      }
    }
  };
  </script>
  
  <style scoped>
  .login-card {
    width: 300px;
    margin: 0 auto;
  }
  label {
    display: block;
    margin: 10px 0;
  }
  button {
    margin-top: 10px;
  }
  </style>
  