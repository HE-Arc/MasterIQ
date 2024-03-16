<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
const API_SERVER = import.meta.env.VITE_API_SERVER;

const imageUrl = ref('');

const fetchImage = async () => {
    const response = await axios.get(`${API_SERVER}/api/category/${props.id}/image/`, { responseType: 'arraybuffer' });
    imageUrl.value = 'data:image/jpeg;base64,' + arrayBufferToBase64(response.data);
}

const arrayBufferToBase64 = (buffer) => {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

const props = defineProps({
    id: Number,
    category: Object
})
onMounted(() => {
    fetchImage();
});
</script>

<template>
    <RouterLink class="link" :to="{ name: 'Quiz', params: { id_category: id } }">
        <div class="category-item" :style="{ backgroundImage: 'url(' + imageUrl + ')' }">
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
