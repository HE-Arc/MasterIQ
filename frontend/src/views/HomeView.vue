<script setup>
import { ref, onMounted } from 'vue';
import CategoryItem from '@/components/CategoryItem.vue';
import LeaderBoard from '@/components/LeaderBoard.vue';
import APIClient from '@/api_client.js';

const categories = ref([]);

onMounted(async () => {
    categories.value = await APIClient.getCategories();
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
        <LeaderBoard />
    </main>
</template>

<style scoped>
.all-categories {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    row-gap: 1rem;
    column-gap: 1.5rem;
}

.btn-container {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
}
</style>
