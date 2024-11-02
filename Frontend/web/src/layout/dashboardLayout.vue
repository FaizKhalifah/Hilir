<template>
    <div class="layoutContainer">
        <dashboardSidebar/>
        <div class="layoutContent">
            <nav>
                <dashboardNavbar/>
            </nav>
            <main>
                <slot>

                </slot>
            </main>
        </div>
    </div>
</template>
<style>
    .layoutContent{
            width: 90%;
        }
    .layoutContainer{
            width: 100%;
            display: flex;
            flex: 1;
    }
    nav{
        background-color: black;
    }
    main{
        padding: 1rem;
    }

</style>
<script>
    import dashboardSidebar from '@/components/sidebar/dashboardSidebar.vue';
    import dashboardNavbar from '@/components/navbar/dashboardNavbar.vue';
    export default{
        name:"dashboardLayoutComponent",
        components:{
            dashboardSidebar,
            dashboardNavbar
        }
    }
</script>