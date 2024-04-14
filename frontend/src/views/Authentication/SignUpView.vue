<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import APIClient from '@/api_client.js';

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const validationMessage = ref('');

const clearForm = () => {
    username.value = '';
    password.value = '';
    confirmPassword.value = '';
    validationMessage.value = '';
};

const register = async () => {
    if (!username.value.trim() || !password.value.trim() || !confirmPassword.value.trim()) {
        validationMessage.value = 'Please fill in all fields.';
        return;
    }

    if (password.value !== confirmPassword.value) {
        validationMessage.value = 'Passwords do not match.';
        return;
    }

    try {
        const response = await APIClient.registerUser(username.value.trim(), password.value.trim());
        console.log('Registration successful:', response);
        validationMessage.value = 'Registration successful.';
        clearForm();
    } catch (error) {
        console.error('Error registering:', error);
        validationMessage.value = 'Error registering. Please try again.';
    }
};
</script>

<template>
    <div>
        <section class="signUp-form container">
            <div>
                <h1 class="title">Register</h1>
                <p class="info">Create a new account</p>
            </div>
            <p :class="{ 'success-message': validationMessage === 'Registration successful.' }">{{ validationMessage }}</p>
            <form @submit.prevent="register" @keyup.enter="register" class="form-wrapper">
                <div class="box">
                    <CustomInput label="Username" v-model="username" required />
                    <CustomInput label="Password" v-model="password" type="password" required />
                    <CustomInput label="Confirm Password" v-model="confirmPassword" type="password" required />
                </div>
                <div class="button-wrapper">
                    <button type="submit" class="btn">Register</button>
                </div>
            </form>
        </section>
    </div>
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
