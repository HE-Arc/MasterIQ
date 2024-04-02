<script setup>
import axios from 'axios';
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

const fetchLeaderboard = async () => {
    // is the global leaderboard
    let url_rank_leaderboard = `/api/rank/global_leaderboard/`;
    let url_rank_user = `/api/rank/global_user/`;

    if (props.id_category !== undefined) {
        // is a category leaderboard
        url_rank_leaderboard = `/api/rank/${props.id_category}/leaderboard/`;
        url_rank_user = `/api/rank/${props.id_category}/user/`;
    }

    const response_leaderboard = await axios.get(url_rank_leaderboard);
    leaderboard.value = response_leaderboard.data;

    const response_user = await axios.get(url_rank_user);
    user_rank.value = response_user.data;
}

onMounted(() => {
    fetchLeaderboard();
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