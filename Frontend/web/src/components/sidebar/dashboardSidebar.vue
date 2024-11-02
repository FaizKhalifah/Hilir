<template>
      <aside>
        <ul>
            <li><router-link to="/admin/dashboard">Overview</router-link></li>
            <li><router-link to="/admin/books">Ruang hilir</router-link></li>
            <li><router-link to="/admin/journals">History</router-link></li>
            <li><router-link to="/admin/employees">Schedule</router-link></li>
            <li><router-link to="/admin/students">Articles</router-link></li>
        </ul>
    </aside>
</template>
<style scoped>
    aside{
        background-color: #010030;
        width: 15%;
        padding: 2rem 0rem;
        padding-bottom: 15rem;
        min-height: 100vh;
    }

    ul{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: flex-start;
        gap: 3rem;
        font-weight: bold;
        list-style-type: none;
    }

    li{
        width: 100%;
        transition: 0.3s;
    }

    a{
        text-decoration: none;
        color: white;
        transition: 0.3s;
        height: 100%;
        width: 100%;
        padding: 1rem;
    }

    a:hover{
        background-color: white;
        color: #010030;
    }
</style>
<script>
    export default{
        name:"psikologSidebarComponent"
    }
</script>