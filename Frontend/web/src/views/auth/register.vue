<template>
    <div class="registerContainer">
        <registerCard/>
    </div>
</template>
<style>
    .registerContainer{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
</style>
<script>
    import registerCard from '@/components/card/registerCard.vue';
    export default{
        name:"registerPage",
        components:{
            registerCard
        }
    }
</script>