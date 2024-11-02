<template>
    <baseCard title="register" cardClass="register-card">
            <form @submit.prevent="handleRegister">
                <div id="fullName">
                <label>Full Name:</label>
                <input type="text" v-model="fullName" />
            </div>
            <div id="email">
                <label>Email : </label>
                <input type="email" v-model="email">
            </div>
            <div id="password">
                <label>Password:</label>
                <input type="password" v-model="password" />
            </div>
            <div id="bio">
                <label>Tell us about your self : </label>
                <textarea v-model="bio"></textarea>
            </div>
            <button type="submit">Login</button>
        </form>
    </baseCard>
</template>
<style scoped>
    .register-card{
        width: 50%;
    }
</style>
<script>
    import baseCard from '../base/baseCard.vue';
    export default{
        name:"registerCardComponent",
        components:{
            baseCard
        },
        data() {
            return {
                fullName : "",
                email: "",
                password: "",
                bio:""
            };
        },
            methods: {
            handleRegister() {
                // Logic untuk login
                console.log("Login dengan:", this.username, this.password);
            }
        }
    }
</script>