<template>
    <div class="loginContainer">
        <loginCard/>
    </div>
</template>
<style>
    .loginContainer{
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
</style>
<script>
    import loginCard from '@/components/card/loginCard.vue';
    export default{
        name:"loginView",
        components:{
            loginCard
        }
    }
</script>