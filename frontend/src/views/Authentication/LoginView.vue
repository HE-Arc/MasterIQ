<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import APIClient from '@/api_client.js';

const username = ref('');
const password = ref('');
const validationMessage = ref('');

const clearForm = () => {
    username.value = '';
    password.value = '';
};

const login = async () => {
    if (!username.value.trim() || !password.value.trim()) {
        validationMessage.value = 'Please fill in all fields.';
        return;
    }

    try {
        const response = await APIClient.loginUser(username.value.trim(), password.value.trim());
        console.log('Login successful:', response);
        validationMessage.value = 'Login successful.';
        clearForm();

        // Redirect or perform additional actions after successful login
    } catch (error) {
        console.error('Error logging in:', error);
        if (error instanceof ValidationError) {
            validationMessage.value = error.message; // Show detailed validation error message to user
        } else {
            validationMessage.value = 'Error logging in. Please try again.';
        }
    }
};
</script>

<template>
    <div>
        <section class="login-form container">
            <h1>Login</h1>
            <p :class="{ 'success-message': validationMessage === 'Login successful.' }">{{ validationMessage }}</p>
            <form @submit.prevent="login" @keyup.enter="login" style="text-align: center;">
                <CustomInput label="Username" v-model="username" required />
                <CustomInput label="Password" v-model="password" type="password" required/>
                <div style="margin-top: 20px;">
                    <button type="submit" class="btn">Login</button>
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
