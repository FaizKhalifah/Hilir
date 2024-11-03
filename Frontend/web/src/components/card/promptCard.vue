<!-- src/components/CardLoginComponent.vue -->
<template>
    <baseCard title="Prompt" cardClass="prompt-card">
        
        <form @submit.prevent="submitPrompt">
            <label >Masukkan apa yang ingin kamu sampaikan ke anak-anak : </label>
            <textarea v-model="message" placeholder="Enter your prompt here" required></textarea>
            <button type="submit" :disabled="loading">Generate</button>
        </form>

        <div v-if="response" class="response">
            <h3>Generated Response:</h3>
            <p>{{ response }}</p>
        </div>
        
        <div v-if="error" class="error">
            <p>Error: {{ error }}</p>
        </div>
    </baseCard>
</template>

<script>
import baseCard from '../base/baseCard.vue';

export default {
    name: "CardLoginComponent",
    components: {
        baseCard
    },
    data() {
        return {
            message: '',
            response: null,
            loading: false,
            error: null
        };
    },
    methods: {
        async submitPrompt() {
            this.loading = true;
            this.error = null;
            this.response = null;

            try {
                const token = localStorage.getItem('token');
                console.log(this.message)
                const response = await fetch("http://127.0.0.1:5000/api/psychologists/chat", {
                    method: "POST",
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message :this.message })
                });
                console.log(response);
                if (!response.ok) {
                    throw new Error("Failed to generate response");
                }

                const data = await response.json();
                this.response = data.bot_response; // Sesuaikan dengan struktur respons API Anda
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>

<style scoped>
.prompt-card {
    padding: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    max-width: 600px;
}

textarea {
    width: 100%;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    resize: vertical;
}

button {
    padding: 0.5rem 1rem;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.response {
    margin-top: 1.5rem;
    background-color: #f9f9f9;
    padding: 1rem;
    border-radius: 4px;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>
