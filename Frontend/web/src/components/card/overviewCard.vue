<template>
    <div class="overview">
        <h2>Overview</h2>
        <div class="summary">
            <div class="childrenCard">
            <p>Total children </p>
            <p>{{ childrenTotal }}</p>
            </div>
            <div class="exerciseCard">
                <p>Total Exercise </p>
                <p>{{ exerciseTotal }}</p>
            </div>
            <div class="assesmentCard">
                <p>Total assesment</p>
                <p>{{ assesmentTotal }}</p>
            </div>
        </div>
        <overviewChart 
        v-if="childrenTotal !== 0 && exerciseTotal !== 0 && assesmentTotal !== 0"
        :childrenTotal="childrenTotal" 
            :exerciseTotal="exerciseTotal" 
            :assesmentTotal="assesmentTotal" 
            />
    </div>
</template>

<style scoped>

.overview {
    padding: 2rem;
}

.summary {
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 2rem;
}

.summary div {
    padding: 1rem 2.5rem;
    border-radius: 1rem;
    color: white;
    background-color: #1985A1;
}
</style>

<script>
import overviewChart from '../chart/overviewChart.vue';
export default {
    name: "overviewCardComponent",
    components:{
        overviewChart
    },
    data() {
        return {
            childrenTotal: 0,
            exerciseTotal: 0,
            assesmentTotal: 0
        };
    },
    mounted() {
        this.fetchChildren();
        this.fetchExercises();
        this.fetchAssignments();
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
                this.childrenTotal = data.length; 
            } catch (err) {
                console.log(err);
            }
        },
        async fetchExercises() {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://127.0.0.1:5000/api/psychologists/exercises', {
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
                this.exerciseTotal = data.length; 
            } catch (err) {
                console.log(err);
            }
        },
        async fetchAssignments() {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://127.0.0.1:5000/api/psychologists/all_assessments', {
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
                this.assesmentTotal = data.length; 
            } catch (err) {
                console.log(err);
            }
        }
    }
};
</script>
