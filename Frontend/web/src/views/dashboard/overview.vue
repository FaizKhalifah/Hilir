<template>
    <dashboardLayout>
        <overviewCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    import overviewCard from '@/components/card/overviewCard.vue';
    export default{
        name:"dashboardOverviewComponent",
        components:{
            dashboardLayout,
            overviewCard
        }
    }
</script>