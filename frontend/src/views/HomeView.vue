<script setup>
import MainLogo from '@/components/icons/FullLogo.vue';
</script>

<template>
    <main class="container center">
        <MainLogo class="logo" />
        <div class="wrapper box">
            <p class="info">Are you looking to improve your IQ in different categories and measure yourself against
                others?
                Whether you're into history, geography, music or film, we've got the perfect quiz for you.
                Answer as many questions as you can to become the IQ master.</p>
            <p class="info">But first, log in to save your progress:</p>
            <RouterLink class="btn" :to="{ name: 'Login' }">Login</RouterLink>
            <RouterLink class="btn" :to="{ name: 'Register' }">Register</RouterLink>
        </div>
    </main>
</template>

<style scoped>

.wrapper {
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
  .logo {
      width: 400px;
      height: 130px;
  }
}
</style>
