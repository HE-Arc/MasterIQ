<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const categories = ref([]);

const fetchCategories = async (query) => {
    const response = await axios.get('http://127.0.0.1:8000/api/category/iq/', {
        params: query
    });
    categories.value = response.data;
    console.log(response);
}

onMounted(() => {
    fetchCategories();
});
</script>

<template>
    <main class="container">
        <h1>This is home page with categories</h1>
        <ul>
            <li v-for="category in categories" :key="category.id">
                {{ category.name }}
            </li>
        </ul>
        <button class="btn">Random question</button>
    </main>
</template>
