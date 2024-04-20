<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref } from 'vue';
import APIClient from '@/api_client.js';
import router from '@/router';

const username = ref('');
const password = ref('');
const validationMessage = ref('');
const loginSuccess = ref(false);

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
        await APIClient.loginUser(username.value.trim(), password.value.trim());

        loginSuccess.value = true;
        validationMessage.value = 'Login successful! Redirecting...';
        clearForm();
        setTimeout(() => {
            validationMessage.value = '';
            router.push('/categories');
        }, 1000);
    }
    catch (error) {
        loginSuccess.value = false;
        validationMessage.value = 'Invalid username or password. Please try again.';
        password.value = '';
    }
};
</script>

<template>
    <div>
        <section class="login-form container">
            <div>
                <h1 class="title">Login</h1>
                <p class="info">Log in here</p>
            </div>
            <p class="form-message" :class="{ 'success-message': loginSuccess }">{{ validationMessage }}</p>
            <form @submit.prevent="login" class="form-wrapper">
                <div class="box">
                    <CustomInput label="Username" v-model="username" required />
                    <CustomInput label="Password" v-model="password" type="password" required />
                </div>
                <div class="button-wrapper">
                    <button type="submit" class="btn">Login</button>
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
    min-height: 80vh;
}

.title,
.info {
    text-align: center;
}

.form-message {
    color: red;
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
