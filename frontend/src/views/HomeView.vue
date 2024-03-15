<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
const API_SERVER = import.meta.env.VITE_API_SERVER;

const categories = ref([]);
console.log(API_SERVER);
const fetchCategories = async (query) => {
    const response = await axios.get(`${API_SERVER}/api/category/iq/`, {
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
                {{ category.category_name }}
            </li>
        </ul>
        <button class="btn">Random question</button>
    </main>
</template>
