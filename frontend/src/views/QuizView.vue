<script setup>
import { useRoute } from 'vue-router';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import AnswerForm from '@/components/AnswerForm.vue';
import LeaderBoard from '@/components/LeaderBoard.vue';
// default variables
const route = useRoute();
const id_category = route.params.id_category;

// variables specific to this component
const question = ref("");

const fetchNewQuestion = async () => {
    const response = await axios.get(`/api/question/${id_category}/new`, {
    });
    question.value = response.data.text;
}

onMounted(() => {
    fetchNewQuestion();
});

</script>

<template>
    <section class="quiz container">
        <p class="info">Answer correctly to the question and earn as many IQs as possible!</p>
        <h1 class="title">Question</h1>
        <p class="question box">{{ question }}</p>
        <AnswerForm @new-question="fetchNewQuestion" />
        <LeaderBoard :id_category="Number(id_category)" />
    </section>
</template>

<style scoped>
.title {
    text-align: center;
    margin-bottom: 1rem;
}

.question {
    text-align: center;
    margin-bottom: 1.3rem;
}
</style>