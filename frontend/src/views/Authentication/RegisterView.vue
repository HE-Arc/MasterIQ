<template>
  <section class="register container">
    <h1>Register</h1>
    <form @submit.prevent="submitForm">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password1" placeholder="Password" required />
      <input type="password" v-model="password2" placeholder="Confirm Password" required />
      <button type="submit" class="btn">Register</button>
    </form>
  </section>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const username = ref('');
const password1 = ref('');
const password2 = ref('');

const submitForm = () => {
  axios.post('/api/register/', {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  })
  .then(response => {
    console.log(response.data);
    // Gérer la réponse du serveur
  })
  .catch(error => {
    console.error(error);
    // Gérer les erreurs
  });
};
</script>
