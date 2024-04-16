<script setup>
import { ref, onMounted } from 'vue';
import CategoryItem from '@/components/CategoryItem.vue';
import LeaderBoard from '@/components/LeaderBoard.vue';
import APIClient from '@/api_client.js';

const categories = ref([]);
const randomId = ref(0);


onMounted(async () => {
    categories.value = await APIClient.getCategories();
    // get a random category id for the random category button
    randomId.value = Math.floor(Math.random() * Object.keys(categories.value).length) + 1;
});
</script>

<template>
    <main class="container col-wrapper">
        <p class="info">Maximise your IQ by correctly answering the questions in the different categories below and
            climb the leaderboard to become the best.</p>
        <div class="empty-space"></div>
        <div>
            <h1 class="title">Categories</h1>
            <div class="all-categories">
                <CategoryItem v-for="category, key in categories" :id="parseInt(key)" :category></CategoryItem>
            </div>
            <div class="btn-container">
                <RouterLink class="btn" :to="{ name: 'Quiz', params: { id_category: randomId } }">Random category</RouterLink>
            </div>
        </div>
        <LeaderBoard />
    </main>
</template>

<style scoped>
.all-categories {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    row-gap: 1rem;
    column-gap: 1rem;
}

.btn-container {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
}

@media (min-width: 1024px) {
    .col-wrapper {
        display: grid;
        grid-template-columns: .66fr .33fr;
        column-gap: 2rem;
    }
}
</style>
