<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import axios from 'axios';

const API_SERVER = import.meta.env.VITE_API_SERVER;

const question = ref('');
const updateQuestion = (value) => {
    question.value = value;
};

const correctAnswer = ref('');
const updateCorrectAnswer = (value) => {
    correctAnswer.value = value;
};

const wrongAnswer1 = ref('');
const updateWrongAnswer1 = (value) => {
    wrongAnswer1.value = value;
};

const wrongAnswer2 = ref('');
const updateWrongAnswer2 = (value) => {
    wrongAnswer2.value = value;
};

const wrongAnswer3 = ref('');
const updateWrongAnswer3 = (value) => {
    wrongAnswer3.value = value;
};

const submitForm = () => {
    axios.post(`${API_SERVER}/api/question/new_community/`, {
        question: question.value,
        options: [correctAnswer.value, wrongAnswer1.value, wrongAnswer2.value, wrongAnswer3.value],
        answer: '0' // Indicate which option is the correct answer.
    })
    .then(response => {
        console.log('Question saved successfully:', response.data);
        // TODO redirect user or show success message
    })
    .catch(error => {
        console.error('Error saving question:', error);
        // TODO handle error
    });
};
</script>

<template>
    <section class="add-question container">
        <h1>Add your question on this page</h1>
        <form @submit.prevent="submitForm">
            <CustomInput label="Question" :value="question.value" @input="updateQuestion" required />
            <CustomInput label="Correct Answer" :value="correctAnswer.value" @input="updateCorrectAnswer" required />
            <CustomInput label="Wrong Answer 1" :value="wrongAnswer1.value" @input="updateWrongAnswer1" required />
            <CustomInput label="Wrong Answer 2" :value="wrongAnswer2.value" @input="updateWrongAnswer2" required/>
            <CustomInput label="Wrong Answer 3" :value="wrongAnswer3.value" @input="updateWrongAnswer3" required/>
            <button type="submit" class="btn">Submit</button>
        </form>
    </section>
</template>
