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

    try {
        const options = [
            correctAnswer.value.trim(),
            wrongAnswer1.value.trim(),
            wrongAnswer2.value.trim(),
            wrongAnswer3.value.trim()
        ];

        const response = await APIClient.postNewCommunityQuestion(question.value.trim(), options);

        console.log('Question saved successfully:', response);
        validationMessage.value = 'Question saved successfully.';
        clearForm();
    } catch (error) {
        console.error('Error saving question:', error);

        if (error instanceof ValidationError) {
            validationMessage.value = error.message; // Show detailed validation error message to user
        } else {
            validationMessage.value = 'Error saving question. Please try again later.';
        }
    }
};
</script>

<template>
    <section class="add-question container form-wrapper">
        <div>
            <h1 class="title">Add your question</h1>
            <p class="info">Help us become the best quiz game ever by adding your amazing new question!</p>
        </div>
        <p :class="{ 'success-message': validationMessage === 'Question saved successfully.' }">{{ validationMessage }}</p>
        <form @submit.prevent="submitForm" class="form-wrapper">
            <div class="box">
                <CustomInput label="Question" v-model="question" required />
            </div>
            <div class="box">
                <CustomInput label="Correct Answer" v-model="correctAnswer" required />
                <CustomInput label="Wrong Answer 1" v-model="wrongAnswer1" required />
                <CustomInput label="Wrong Answer 2" v-model="wrongAnswer2" required />
                <CustomInput label="Wrong Answer 3" v-model="wrongAnswer3" required />
            </div>
            <div class="button-wrapper">
                <button type="submit" class="btn">Submit</button>
            </div>
        </form>
    </section>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.title, .info {
    text-align: center;
}

.success-message {
    color: green;
}

@media (min-width: 576px) {
    .form-wrapper {
        max-width: 90%;
    }
}


@media (min-width: 1024px) {
    .form-wrapper {
        max-width: 70%;
    }
}

</style>

