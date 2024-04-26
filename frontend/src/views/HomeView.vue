<script setup>
import MainLogo from '@/components/icons/FullLogo.vue';
import {getTokenFromCookie} from "@/api_client.js";
import {onMounted, ref} from "vue";

const isConnected = ref(false);

onMounted(() => {
    const token = getTokenFromCookie();

    if (token !== undefined) {
        isConnected.value = true;
    } else {
        isConnected.value = false;
    }
});
</script>

<template>
    <main class="container">
        <MainLogo class="logo" />
        <div class="info-wrapper box">
            <p class="info">Are you looking to improve your IQ in different categories and measure yourself against
                others?
                Whether you're into history, geography, music or film, we've got the perfect quiz for you.
                Answer as many questions as you can to become the IQ master.</p>
            <div v-if="isConnected">
              <RouterLink class="btn" :to="{ name: 'Categories' }">Categories</RouterLink>
              <RouterLink class="btn" :to="{ name: 'Add question' }">Add question</RouterLink>
            </div>
            <div v-else>
              <p class="info">But first, log in to save your progress:</p>
              <RouterLink class="btn" :to="{ name: 'Login' }">Login</RouterLink>
              <RouterLink class="btn" :to="{ name: 'Register' }">Register</RouterLink>
            </div>
        </div>
    </main>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.info-wrapper {
    text-align: center;
}

.info:first-child {
    margin-top: 0;
}

.btn {
    display: block;
    flex-direction: column;
    margin-top: 1rem;
}

.logo {
    width: 300px;
    height: 150px;
}

@media (min-width: 576px) {
    .info-wrapper {
        max-width: 80%;
    }

    .logo {
        width: 400px;
        height: 130px;
    }
}

@media (min-width: 1024px) {
    .info-wrapper {
        max-width: 50%;
    }
}
</style>
