<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import APIClient from '@/api_client.js';
import router from '@/router';

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const validationMessage = ref('');
const registerSuccess = ref(false);

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
        await APIClient.registerUser(username.value.trim(), password.value.trim());
        validationMessage.value = "Registration successful! Redirecting...";
        registerSuccess.value = true;
        setTimeout(() => {
            validationMessage.value = '';
            router.push('/categories');
        }, 1000);
        clearForm();
    } catch (error) {
        registerSuccess.value = false;
        validationMessage.value = "Username already exists!";
    }
};
</script>

<template>
    <main class="container center">
        <section class="wrapper">
            <div>
                <h1 class="title">Register</h1>
                <p class="info">Create a new account</p>
            </div>
            <p class="form-message" :class="{ 'success-message': registerSuccess }">{{ validationMessage }}</p>
            <form @submit.prevent="register">
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
    </main>
</template>

<style scoped>
.wrapper {
    min-width: 50%;
}

.title,
.info {
    text-align: center;
}

.form-message {
    color: red;
    text-align: center;
    margin-bottom: .5rem;
}

.success-message {
    color: green;
}
</style>
