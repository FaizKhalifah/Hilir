<template>
    <baseCard title="Schedule " card-class="scheduleCard">
        <div class="schedule">
            <ul>
                <li v-for="s in schedule" :key="s.available_on_date">
                <div  class="scheduleDiv">
                        <p>Waktu mulai : {{ s.start_time }}</p>
                        <p>Waktu selesai : {{ s.end_time }}</p>
                        <br><br>
                    </div>
                </li>
            </ul>
        </div>
    </baseCard>
</template>
<style scoped>
    *{
        color: black;
    }
</style>
<script>
    import baseCard from '../base/baseCard.vue';
    export default{
        name:"scheduleCardComponent",
        components:{
            baseCard
        },
        data(){
            return{
                schedule:[]
            }
        },
        mounted() {
            this.fetchSchedule();
  },
  methods: {
    async fetchSchedule() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/psychologists/schedule', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`, 
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        console.log(data)
        console.log(data.schedule)
        this.schedule = data.schedule;
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
}
}
</script>