<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

import router from './router'
import { getTokenFromCookie } from './api_client';
import { ref } from 'vue';

const isConnected = ref(false);

router.beforeEach(async (to, from, next) => {
    const token = getTokenFromCookie();

    // check if token exists
    if (token !== undefined) {
        isConnected.value = true;
    } else {
        isConnected.value = false;
    }

    // redirection if necessary
    if (to.meta.requiresAuth) {
        if (token !== undefined) {
            next();
        } else {
            next('/'); // redirect to home page
        }
    } else {
        next();
    }
})
</script>

<template>
    <Header :is-connected="isConnected" />
    <RouterView />
    <Footer />
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bevan:ital@0;1&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
</style>
