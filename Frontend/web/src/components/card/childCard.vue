<template>
    <baseCard title="Ruang Hilir" card-class="childCard">
    <div class="childrenList">
        <ul v-if="children.length">
            
            <li v-for="child in children" :key="child.child_id">
            <div  class="childDiv">
                <div class="childrenData">
                    <h1>{{ child.name }}</h1>
                    <p>Age: {{ child.age }}</p>
                    <p>Gender: {{ child.gender }}</p>
                    <br><br>
                    <a @click="fetchChildDetail(child.child_id)">Detail</a>
                </div>
                <img :src="require('@/assets/Home.png')" alt="">
            </div>
            </li>
        </ul>
        <p v-else>Loading...</p>
    </div>

    <!-- Modal untuk detail anak -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Child Details</h3>
        <p v-if="childDetail">Name: {{ childDetail.name }}</p>
        <p>Age: {{ childDetail.age }}</p>
        <p>Gender: {{ childDetail.gender }}</p>
        <p>Report: {{ childDetail.report }}</p>
        <button @click="goToAssessment" style="margin-top: 1rem;">Go to Assessment</button>
        <button @click="goToExercise">Go to Exercise</button>
        <button @click="closeModal">Close</button>
      </div>
    </div>

    </baseCard>
   
</template>
<style scoped>
    *{
        color: black;
    }

    .childCard{
        border-width: 2px;
    }

    .modal {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        transition: 0.3s;
        }

    .modal-content {
        background-color: white;
        padding: 2rem;
        border-radius: 5px;
        width: 80%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .modal-content button{
        background-color: #010030;
        color: white;
        transition: 0.3s;
        border: 1px solid white;
        cursor: pointer;
        padding: 0.75rem 0rem;
        border-radius: 1rem;
        width: 15rem;
    }

    .modal-content button:hover{
        color: #010030;
        background-color: white;
        border-color: #010030;
    }

    .close {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 18px;
        cursor: pointer;
    }

    .childDiv{
        background-color: white;
        border: 1px solid #010030;
        padding: 2rem;
        border-radius: 1rem;
        cursor: pointer;
        width: 25rem;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }

    .childDiv img{
        width: 40%;
    }
    ul{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 1rem;
    }

    ul a{
        background-color: #010030;
        padding: 0.5rem 2rem;
        border-radius: 1rem;
        transition: 0.3s;
        cursor: pointer;
        border: 1px solid white;
        color: white;
    }

    a:hover{
        background-color: white;
        border-color: #010030;
        color: #010030;
    }
</style>
<script>
import baseCard from '../base/baseCard.vue';
    export default{
        name:"childCardComponent",
        components:{
            baseCard
        },
        data() {
    return {
      children: [],
      childDetail: null, // Objek untuk menyimpan detail anak
      showModal: false, 
    };
  },
  mounted() {
    this.fetchChildren();
  },
  methods: {
    async fetchChildren() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/psychologists/all_children', {
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
        this.children = data;
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchChildDetail(childId) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/api/psychologists/child/${childId}/report`, {
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
        this.childDetail = data; // Menyimpan data detail anak ke childDetail
        this.showModal = true; // Menampilkan modal
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    closeModal() {
      this.showModal = false; // Menyembunyikan modal
      this.childDetail = null; // Mengosongkan data detail
    },
    goToAssessment() {
      // Arahkan ke halaman Assessment dengan child_id
      this.$router.push({ name: 'Assessment', params: { child_id: this.childDetail.child_id } });
    },
    goToExercise() {
      // Arahkan ke halaman Exercise dengan child_id
      this.$router.push({ name: 'Exercise', params: { child_id: this.childDetail.child_id } });
    }
    }
}
</script>