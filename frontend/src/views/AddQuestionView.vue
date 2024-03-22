<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import axios from 'axios';

const API_SERVER = import.meta.env.VITE_API_SERVER;

const question = ref('');
const correctAnswer = ref('');
const wrongAnswer1 = ref('');
const wrongAnswer2 = ref('');
const wrongAnswer3 = ref('');
const validationMessage = ref('');
const clearForm = () => {
    question.value = '';
    correctAnswer.value = '';
    wrongAnswer1.value = '';
    wrongAnswer2.value = '';
    wrongAnswer3.value = '';
};

const submitForm = () => {
    if (!question.value.trim() || !correctAnswer.value.trim() || !wrongAnswer1.value.trim()
        || !wrongAnswer2.value.trim() || !wrongAnswer3.value.trim()) {
        validationMessage.value = 'Please fill in all fields.';
        return;
    }

    if (question.value.length > 250 || correctAnswer.value.length > 250 || wrongAnswer1.value.length > 250
        || wrongAnswer2.value.length > 250 || wrongAnswer3.value.length > 250) {
        validationMessage.value = 'Input fields cannot exceed 250 characters.';
        return;
    }

    axios.post(`${API_SERVER}/api/question/new_community/`, {
        question: question.value.trim(),
        options: [correctAnswer.value.trim(), wrongAnswer1.value.trim(), wrongAnswer2.value.trim(), wrongAnswer3.value.trim()],
        answer: '0' // Indicate which option is the correct answer.
    })
    .then(response => {
        console.log('Question saved successfully:', response.data);
        validationMessage.value = 'Question saved successfully.';
        clearForm();
    })
    .catch(error => {
        console.error('Error saving question:', error);
        validationMessage.value = 'Error saving question. Please try again later.';
        // TODO: Show detail error message to user
    });
};
</script>


<template>
    <section class="add-question container">
        <h1>Add your question on this page</h1>
        <!--For mid eval only-->
        <p :class="{ 'success-message': validationMessage === 'Question saved successfully.' }">{{ validationMessage }}</p>
        <form @submit.prevent="submitForm">
            <CustomInput label="Question" v-model="question" required />
            <CustomInput label="Correct Answer" v-model="correctAnswer" required />
            <CustomInput label="Wrong Answer 1" v-model="wrongAnswer1" required />
            <CustomInput label="Wrong Answer 2" v-model="wrongAnswer2" required/>
            <CustomInput label="Wrong Answer 3" v-model="wrongAnswer3" required/>
            <button type="submit" class="btn">Submit</button>
        </form>
    </section>
</template>

// For mid eval only
<style>
.success-message {
    color: green;
}
</style>