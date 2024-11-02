<template>
    <baseCard title="Login" cardClass="login-card">
      <div class="loginContent">
        <form @submit.prevent="handleLogin">
          <div class="email">
            <label>
            Email:
            </label>
            <input type="text" v-model="email" />
          </div>
          <div class="password">
          <label>
            Password:
          </label>
          <input type="password" v-model="password" />
          </div>
          <div class="register">
            <p>Dont have an account? Register  <a href="/register">here</a></p>
          </div>
        <button type="submit">Login</button>
      </form>
      <img :src="require('@/assets/login.png')" alt="">
      </div>
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
      async handleLogin() {
        const userData = {
          email:this.email,
          password:this.password
        }
        console.log(userData)
        try{
          const response = await fetch('http://127.0.0.1:5000/api/psychologists/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            console.log(response);
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            const data = await response.json();
            if(data){
              localStorage.setItem('token', data.token);
              console.log('Success:', data);
              this.$router.push('/dashboard');
            }
        }catch(err){
          console.log(err);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-card {
    width: 70%;
    margin: 2rem 0rem;
  }
 
  .loginContent {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    form{
        margin-top: 2rem;
        width: 60%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 2rem;
    }

    form div{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    img{
        width: 40%
    }

    input, button{
        width: 25rem;
    }
    
    button{
        background-color: #010030;
        color: white;
        transition: 0.3s;
        border: 1px solid white;
        cursor: pointer;
        padding: 0.75rem 0rem;
        border-radius: 1rem;
    }

    button:hover{
        color: #010030;
        background-color: white;
        border-color: #010030;
    }


  </style>
  