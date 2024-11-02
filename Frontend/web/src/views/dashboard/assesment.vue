<template>
    <dashboardLayout>
        <assesmentCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import assesmentCard from '@/components/card/assesmentCard.vue';
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    export default{
        name:"assesmentComponent",
        components:{
            assesmentCard,
            dashboardLayout
        }
    }
</script>