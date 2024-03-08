<script setup>
import CustomInput from '@/components/CustomInput.vue';
import { ref, computed } from 'vue';

const username = ref('');
const updateUsername = (value) => {
    username.value = value;
};

const password = ref('');
const updatePassword = (value) => {
    password.value = value;
};

const submitForm = () => {
    console.log('Form submitted');
    // TODO call api
};

</script>
<template>
    <section class="login">
        <h1>This is login page</h1>
        <form @submit.prevent="submitForm">
            {{ username }} <!-- TODO debug purpose remove this line -->
            <CustomInput label="Username" :value="username" @input="updateUsername" required />
            {{ password }} <!-- TODO debug purpose remove this line -->
            <CustomInput label="Password" type="password" :value="password" @input="updatePassword" required />
            <button type="submit" class="btn">Submit</button>
        </form>
    </section>
</template>