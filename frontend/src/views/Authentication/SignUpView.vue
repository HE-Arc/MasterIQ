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
        <section class="register-form container">
            <h1>Register</h1>
            <p :class="{ 'success-message': validationMessage === 'Registration successful.' }">{{ validationMessage }}</p>
            <form @submit.prevent="signUp" @keyup.enter="signUp" style="text-align: center;">
                <CustomInput label="Username" v-model="username" required />
                <CustomInput label="Password" v-model="password" type="password" required />
                <CustomInput label="Confirm Password" v-model="confirmPassword" type="password" required />
                <div style="margin-top: 20px;">
                    <button type="submit" class="btn">Register</button>
                </div>
            </form>
        </section>
    </div>
</template>


<style>
.success-message {
    color: green;
}
</style>
