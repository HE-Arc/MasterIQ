<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import CategoryItem from '@/components/CategoryItem.vue';
const API_SERVER = import.meta.env.VITE_API_SERVER;

const categories = ref([]);

const fetchCategories = async (query) => {
    const response = await axios.get(`${API_SERVER}/api/category/iq/`, {
        params: query
    });
    categories.value = response.data;
}

onMounted(() => {
    fetchCategories();
});
</script>

<template>
    <main class="container">
        <p class="info">Maximise your IQs in each question category and climb the overall rankings.</p>
        <h1 class="title">Categories</h1>
        <div class="all-categories">
            <CategoryItem v-for="category, key in categories" :id="parseInt(key)" :category></CategoryItem>
        </div>
        <div class="btn-container">
            <button class="btn">Random question</button>

        </div>
    </main>
</template>

<style scoped>
.all-categories {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    row-gap: 1rem;
    column-gap: 1.5rem;
}

.info {
    margin: 1.5rem 0 1rem 0;
}

.btn-container {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
}
</style>
