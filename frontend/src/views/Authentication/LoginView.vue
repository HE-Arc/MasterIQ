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
    <main class="container center">
        <section class="wrapper">
            <div>
                <h1 class="title">Login</h1>
                <p class="info">Log in here</p>
            </div>
            <p class="form-message" :class="{ 'success-message': loginSuccess }">{{ validationMessage }}</p>
            <form @submit.prevent="login">
                <div class="box">
                    <CustomInput label="Username" v-model="username" required />
                    <CustomInput label="Password" v-model="password" type="password" required />
                </div>
                <div class="button-wrapper">
                    <button type="submit" class="btn">Login</button>
                </div>
            </form>
        </section>
    </main>
</template>

<style scoped>
.title,
.info {
    text-align: center;
}

.wrapper
{
    min-width: 50%;
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
