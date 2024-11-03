<template>
    <dashboardLayout>
        <scheduleCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    import scheduleCard from '@/components/card/scheduleCard.vue';
    export default{
        name:"scheduleComponent",
        components:{
            dashboardLayout,
            scheduleCard
        }
    }
</script>