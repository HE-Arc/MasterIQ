<script setup>
import CustomInput from '@/components/CustomInput.vue';
import APIClient from '@/api_client.js';
import { ref } from 'vue';

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

const submitForm = async () => {
    validationMessage.value = '';
    try {
        if (!question.value.trim() || !correctAnswer.value.trim() || !wrongAnswer1.value.trim()
            || !wrongAnswer2.value.trim() || !wrongAnswer3.value.trim()) {
            validationMessage.value ='Please fill in all fields. ';
        }

        if (question.value.length > 250 || correctAnswer.value.length > 250 || wrongAnswer1.value.length > 250
            || wrongAnswer2.value.length > 250 || wrongAnswer3.value.length > 250) {
            validationMessage.value = 'Input fields cannot exceed 250 characters. ';
        }

        const options = [
            correctAnswer.value.trim(),
            wrongAnswer1.value.trim(),
            wrongAnswer2.value.trim(),
            wrongAnswer3.value.trim()
        ];

        const response = await APIClient.postNewCommunityQuestion(question.value.trim(), options);

        validationMessage.value = 'Question saved successfully.';
    } catch (error) {
        validationMessage.value += 'Failed to save question. Please try again.';
        console.error('Error saving question:', error.message);
    }
  clearForm();
};
</script>

<template>
    <section class="center container form-wrapper">
        <div>
            <h1 class="title">Add your question</h1>
            <p class="info">Help us become the best quiz game ever by adding your amazing new question!</p>
        </div>
        <form @submit.prevent="submitForm" class="form-wrapper">
            <div class="box">
                <CustomInput label="Question" v-model="question" required />
            </div>
            <div class="box">
                <CustomInput label="Correct Answer" v-model="correctAnswer" required />
                <CustomInput label="Wrong Answer 1" v-model="wrongAnswer1" required />
                <CustomInput label="Wrong Answer 2" v-model="wrongAnswer2" required />
                <CustomInput label="Wrong Answer 3" v-model="wrongAnswer3" required />
                <p class="info" :style="{ color : validationMessage === 'Question saved successfully.' ?
                    'green' : 'red'}">{{ validationMessage }}</p>
            </div>
            <div class="button-wrapper">
                <button type="submit" class="btn">Submit</button>
            </div>
        </form>
    </section>
</template>

<style scoped>
.title, .info {
    text-align: center;
}
</style>

