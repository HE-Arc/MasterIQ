<script setup>
import APIClient from '@/api_client';
import { onMounted, ref } from 'vue';

const imageData = ref('');

const props = defineProps({
    id: Number,
    category: Object
})
onMounted(async () => {
    imageData.value = await APIClient.getImageCategory(props.id);
});
</script>

<template>
    <RouterLink class="link" :to="{ name: 'Quiz', params: { id_category: id } }">
        <div class="category-item" :style="{ backgroundImage: 'url(' + imageData + ')' }">
            <div class="opacity-filter">
                <h2 class="name">{{ category.category_name }}</h2>
                <p class="iq">{{ category.user_iq }}</p>
            </div>
        </div>
    </RouterLink>
</template>

<style scoped style="scss">
.link
{
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease-in-out;
    &:hover
    {
        transform: scale(1.05);
    }
}
.category-item {
    border-radius: 1.5rem;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    height: 100%;

    .opacity-filter {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem 1rem;
        border-radius: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .name {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        font-style: italic;
    }

    .iq {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
    }
}
</style>
