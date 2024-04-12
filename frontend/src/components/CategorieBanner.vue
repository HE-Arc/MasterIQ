<script setup>
import APIClient from '@/api_client';
import { onMounted, defineProps, ref } from 'vue';

const imageData = ref('');
const imageLoaded = ref(false);

const categoryName = ref('');

const props = defineProps({
    id_category: Number
})

onMounted(async () => {
    imageData.value = await APIClient.getImageCategory(props.id_category);
    imageLoaded.value = true;

    categoryName.value = await APIClient.getCategoryName(props.id_category);
});
</script>

<template>
    <Transition>
        <div v-if="imageLoaded">
            <h2 class="title">Categorie</h2>
            <div class="category-banner" :style="{ backgroundImage: 'url(' + imageData + ')' }">
                <div class="opacity-filter">
                    <span class="category-name">{{ categoryName }}</span>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style scoped style="scss">
.v-enter-active,
.v-leave-active {
    transition: all 1s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

.category-banner {
    border-radius: 1.5rem;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    margin-bottom: 1.3rem;

    .opacity-filter {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 1rem;
        border-radius: 1.5rem;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

        .category-name {
            font-family: 'Montserrat', Inter, sans-serif;
            font-weight: 800;
            color: black;
            font-size: 1.75rem;
            font-style: italic;
            color: white;
            text-transform: uppercase;
        }
    }
}
</style>
