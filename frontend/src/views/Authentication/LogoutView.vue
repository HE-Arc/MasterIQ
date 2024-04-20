<script setup>
import { onMounted } from 'vue';
import APIClient from '@/api_client.js';
import router from '@/router';

onMounted(async () => {
    await APIClient.logoutUser();
    setTimeout(() => {
        router.push('/');
    }, 1000);
});
</script>

<template>
    <main class="container">
        <h1 class="title">Disconnecting...</h1>
    </main>
</template>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>