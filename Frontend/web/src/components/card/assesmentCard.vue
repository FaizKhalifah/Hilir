<template>
    <baseCard title="Assessment" card-class="assesmentCard">
        <form @submit.prevent="submitAssignment">
            <div>
                <label>Task Name:</label>
                <input type="text" v-model="form.task_description" />
            </div>
            <div>
                <label>Due Date:</label>
                <input type="date" v-model="form.due_date" required />
            </div>
            <div>
                <label>Frequency (in hours):</label>
                <input type="number" v-model="form.frequency" required />
            </div>
            
            <div v-for="(question, qIndex) in form.questions" :key="`question-${qIndex}`" class="question">
                <div class="questionContent">
                    <label>Question:</label>
                    <input type="text" v-model="question.question" placeholder="Question" required />

                    <div v-for="(impact, iIndex) in question.impacts" :key="`impact-${qIndex}-${iIndex}`" class="impact">
                        <label>Impact for Issue ID:</label>
                        <input
                            type="number"
                            v-model="impact.mental_health_issue_id"
                            placeholder="Issue ID"
                            required
                        />
                        <label>Score Impact:</label>
                        <input
                            type="number"
                            v-model="impact.score_impact"
                            placeholder="Score Impact"
                            required
                        />
                        <div id="impactButton">
                            <button type="button" @click="removeImpact(qIndex, iIndex)">Remove Impact</button>
                            <button type="button" @click="addImpact(qIndex)">Add Impact</button>
                        </div>
                    </div>
                </div>
                <div id="questionButton">
                    <button type="button" @click="removeQuestion(qIndex)">Remove Question</button>
                    <button type="button" @click="addQuestion">Add Question</button>
                </div>
            </div>
            <button type="submit">Submit Assignment</button>
        </form>
    </baseCard>
</template>

<script>
import baseCard from '../base/baseCard.vue';

export default {
    name: "AssessmentCardComponent",
    components: {
        baseCard
    },
    data() {
        return {
            form: {
                task_description: '',
                due_date: '',
                frequency: 24,
                questions: [
                    {
                        question: '',
                        impacts: [
                            { mental_health_issue_id: '', score_impact: '' }
                        ]
                    }
                ]
            }
        };
    },
    methods: {
        addQuestion() {
            this.form.questions.push({
                question: '',
                impacts: [{ mental_health_issue_id: '', score_impact: '' }]
            });
        },
        removeQuestion(index) {
            this.form.questions.splice(index, 1);
        },
        addImpact(questionIndex) {
            this.form.questions[questionIndex].impacts.push({ mental_health_issue_id: '', score_impact: '' });
        },
        removeImpact(questionIndex, impactIndex) {
            this.form.questions[questionIndex].impacts.splice(impactIndex, 1);
        },
        async submitAssignment() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(
                    'http://127.0.0.1:5000/api/psychologists/child/1/add_assessment_with_questions',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`
                        },
                        body: JSON.stringify(this.form)
                    }
                );
                
                if (!response.ok) throw new Error('Failed to submit assignment');

                alert('Assignment submitted successfully');
                this.resetForm(); // Reset form setelah submit berhasil
                this.$router.push('/ruanghilir');
            } catch (error) {
                console.error(error);
                alert('Failed to submit assignment');
            }
        },
        resetForm() {
            this.form = {
                task_description: '',
                due_date: '',
                frequency: 24,
                questions: [
                    {
                        question: '',
                        impacts: [{ mental_health_issue_id: '', score_impact: '' }]
                    }
                ]
            };
        }
    }
};
</script>

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
    padding: 0.75rem 0rem;
    border-radius: 1rem;
    width: 15rem;
}

.questionContent {
    border: 1px solid gray;
    padding: 1rem 1.5rem 2rem;
    display: flex;
    flex-direction: column;
}

#impactButton, #questionButton {
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

#impactButton button, #questionButton button {
    width: 10rem;
}
</style>
