<script setup>
import APIClient from '@/api_client';
import IconMedal from './icons/IconMedal.vue';
import { onMounted, ref } from 'vue';

const imageData = ref('');
const imageLoaded = ref(false);

const props = defineProps({
    id: Number,
    category: Object
})

const colorFromIQ = (iq) => {
    if (iq < 100) {
        return null;
    } else if (iq < 120) {
        return '#CD7F32';
    } else if (iq < 170) {
        return '#C0C0C0';
    } else {
        return '#FFD700';
    }
}

onMounted(async () => {
    imageData.value = await APIClient.getImageCategory(props.id);
    imageLoaded.value = true;
});
</script>

<template>
    <Transition>
        <RouterLink v-if="imageLoaded" class="link" :to="{ name: 'Quiz', params: { id_category: id } }">
            <div class="category-item" :style="{ backgroundImage: 'url(' + imageData + ')' }">
                <div class="opacity-filter">
                    <h2 class="name">{{ category.category_name }}</h2>
                    <p class="iq">{{ category.user_iq }}</p>
                </div>
                <IconMedal class="icon-medal" :rgb_color="colorFromIQ(category.user_iq)" />
            </div>
        </RouterLink>
    </Transition>
</template>

<style scoped style="scss">
.v-enter-active,
.v-leave-active {
    transition: all 1s ease !important;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

.link {
    text-decoration: none;
    color: inherit;
    transition: transform 0.3s ease-in-out;

    &:hover {
        transform: scale(1.05);
    }
}

.category-item {
    border-radius: 1.5rem;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    height: 100%;
    position: relative;

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

    .icon-medal
    {
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        width: 35px;
    }
}
</style>
