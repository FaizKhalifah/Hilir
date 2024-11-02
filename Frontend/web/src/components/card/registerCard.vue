<template>
    <baseCard title="Register" cardClass="register-card">
        <div class="registerContent">
            <form @submit.prevent="handleRegister">
            <div id="fullName">
                <label>Full Name:</label>
                <input type="text" v-model="full_name" />
            </div>
            <div id="email">
                <label>Email : </label>
                <input type="email" v-model="email">
            </div>
            <div id="password">
                <label>Password:</label>
                <input type="password" v-model="password" />
            </div>
            <div id="specialization">
                <label>Your specialization : </label>
                <select v-model="specialization" >
                    <option value="ADHD">ADHD</option>
                    <option value="autism">Autism</option>
                    <option value="anxiety">Anxiety</option>
                </select>
            </div>
            <div id="bio">
                <label>Tell us about your self : </label>
                <textarea v-model="bio"></textarea>
            </div>
            
            <button type="submit">Register</button>
            </form>
            <img :src="require('@/assets/register.png')" alt="">
        </div>
    </baseCard>
</template>
<style scoped>
    .register-card{
        width: 70%;
        margin: 2rem 0rem;
    }

    .registerContent {
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

    input, textarea, select, button{
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

    textarea{
        height: 15rem;
        padding: 0.5rem;
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
                full_name : "",
                email: "",
                password: "",
                specialization:"",
                bio:""
            };
        },
            methods: {
            async handleRegister() {
                const userData = {
                    full_name: this.full_name,
                    email: this.email,
                    password: this.password,
                    specialization:this.specialization,
                    bio: this.bio
                };
                console.log(userData);
                try{
                    const response = await fetch('http://127.0.0.1:5000/api/psychologists/register', {
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
                        console.log('Success:', data);
                        this.$router.push('/dashboard');
                    }
                   

                }catch(err){
                    console.log(err);
                }
            }
        }
    }
</script>