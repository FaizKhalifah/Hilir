<template>
    <baseCard title="Login" cardClass="login-card">
      <form @submit.prevent="handleLogin">
        <label>
          Username:
          <input type="text" v-model="username" />
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
        username: "",
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
  
  <style>
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
  