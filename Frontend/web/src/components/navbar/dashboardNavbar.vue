<template>
    <ul>
        <li>Dashboard Psikolog</li>
            <li>
                <div class="searchBar">
                    <div class="searchForm">
                        <form action="">
                            <input type="text" name="search" id="search" placeholder="search">
                        </form>
                        <button>Search</button>
                    </div>
                    <a @click.prevent="logout">Logout</a>
                </div>
            </li>
    </ul>
</template>
<style>
    ul, .searchBar, .searchForm{
        list-style-type: none;
        display: flex;
        flex-direction: row;
    }

    ul{
        align-items: center;
        justify-content: space-between;
        gap: 10rem;
        padding: 1rem;
    }

    .searchBar{
        align-items: center;
        gap: 2rem;
    }

    .searchForm{
        gap: 0rem;
        align-items: stretch;
    }

    .searchForm button{
        padding: 0rem 1.1rem;
        background-color: #EC9A29;
        color: white;
        border: none;
    }

    .searchBar a{
        text-decoration: none;
        color: white;
        cursor: pointer;
    }

    nav input[type=text]{
        padding: 0.5rem 1rem;
    }

    li{
        color: white;
    }

</style>
<script>
    export default{
        name:"dashboardNavbarComponent",
        methods:{
          logout(){
            localStorage.removeItem('token'); // Hapus token dari localStorage
            this.$router.push({ name: 'login' }); // Arahkan ke halaman login
        }
        }
    }
</script>