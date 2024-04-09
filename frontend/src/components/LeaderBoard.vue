<script setup>
import APIClient from '@/api_client';
import { defineProps, onMounted, ref } from 'vue';

const props = defineProps({
    // if id_category is null, show the global leaderboard
    id_category: {
        type: Number,
        required: false,
    }
})

const leaderboard = ref([]);
const user_rank = ref(null);

onMounted(async () => {
    if (props.id_category !== undefined) {
        // is a category leaderboard
        leaderboard.value = await APIClient.getCategoryLeaderboard(props.id_category);
        user_rank.value = await APIClient.getCategoryUserRank(props.id_category);
    }
    else
    {
        // is the global leaderboard
        leaderboard.value = await APIClient.getGlobalLeaderboard();
        user_rank.value = await APIClient.getGlobalUserRank();
    }
});

</script>

<template>
    <div class="leaderboard">
        <h2 class="title">Leaderboard</h2>
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>IQ</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(user, key) in leaderboard" :key="user.id">
                    <td>{{ key + 1 }}</td>
                    <td>{{ user.user_name }}</td>
                    <td>{{ user.user_iq }}</td>
                </tr>
                <tr v-if="user_rank" class="player-rank">
                    <td>{{ user_rank.user_rank }}</td>
                    <td>YOU</td>
                    <td>{{ user_rank.user_iq }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.leaderboard-table {
    border-collapse: collapse;
    border-radius: 20px;
    overflow: hidden;

    background-color: #F6F6F6;
    width: 100%;

    td {
        padding: 0.3rem 0;
        text-align: center;
    }

    .player-rank {
        border-top: 1px solid #000;

        td {
            padding: 0.5rem 0;
        }
    }

    thead {

        tr {
            background-color: var(--miq-aqua);
            color: white;

            th {
                font-size: 1rem;
                font-weight: bold;
                padding: 0.5rem 0;
            }
        }
    }
}
</style>