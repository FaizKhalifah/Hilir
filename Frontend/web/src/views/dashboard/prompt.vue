<template>
    <dashboardLayout>
        <promptCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    import promptCard from '@/components/card/promptCard.vue';
    export default{
        name:"promptComponent",
        components:{
            dashboardLayout,promptCard
        }
    }
</script>