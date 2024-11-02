<template>
    <dashboardLayout>
        <exerciseCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import exerciseCard from '@/components/card/exerciseCard.vue';
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    export default{
        name:"exerciseComponent.vue",
        components:{
            exerciseCard,
            dashboardLayout
        }
    }
</script>