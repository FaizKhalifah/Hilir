<template>
    <baseCard title="exercise" card-class="exerciseCard">
        <form @submit.prevent="submitExercise">
            <div>
                <label>Title:</label>
                <input type="text" v-model="form.title" required />
            </div>
            <div>
                <label>Description:</label>
                <input type="text" v-model="form.description" required />
            </div>
            <div>
                <label>Mental health issue ID:</label>
                <input type="number" v-model="form.mental_health_issue_id" required />
            </div>
            <div>
                <label>Assigned date:</label>
                <input type="date" v-model="form.assigned_date" required />
            </div>
            <button type="submit">Submit exercise</button>
        </form>
    </baseCard>
</template>

<style scoped>
    form {
        margin-top: 2rem;
        width: 60%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 2rem;
    }

    form div {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    button {
        background-color: #010030;
        color: white;
        transition: 0.3s;
        border: 1px solid white;
        cursor: pointer;
        padding: 1rem 2rem;
        border-radius: 1rem;
    }

    button:hover {
        color: #010030;
        background-color: white;
        border-color: #010030;
    }
</style>

<script>
import baseCard from '../base/baseCard.vue';

export default {
    name: "exerciseCardComponent",
    components: {
        baseCard
    },
    data() {
        return {
            form: {
                title: '',
                description: '',
                mental_health_issue_id: '',
                assigned_date: ''
            }
        };
    },
    methods: {
        async submitExercise() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(
                    'http://127.0.0.1:5000/api/psychologists/child/1/assign_exercise',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`
                        },
                        body: JSON.stringify(this.form)
                    }
                );

                if (!response.ok) throw new Error('Failed to submit exercise');

                alert('Exercise submitted successfully');
                this.resetForm();
                this.$router.push('/ruanghilir');
            } catch (error) {
                console.error(error);
                alert('Failed to submit exercise');
            }
        },
        resetForm() {
            this.form = {
                title: '',
                description: '',
                mental_health_issue_id: '',
                assigned_date: ''
            };
        }
    }
};
</script>
