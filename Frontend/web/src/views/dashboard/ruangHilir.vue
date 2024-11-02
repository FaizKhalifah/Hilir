<template>
    <dashboardLayout>
        <childCard/>
    </dashboardLayout>
</template>
<style>

</style>
<script>
    import dashboardLayout from '@/layout/dashboardLayout.vue';
    import childCard from '@/components/card/childCard.vue';
    export default{
        name:"ruangHilirComponent",
        components:{
            dashboardLayout,
            childCard
        }
    }
</script>