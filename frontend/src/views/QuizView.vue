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
const question = ref(null);
const hasAskedOptions = ref(false);

const fetchNewQuestion = async () => {
    const responseQuestion = await axios.get(`/api/question/${id_category}/new`, {
    });
    question.value = responseQuestion.data.text;

    // wait for the question before checking if the user has asked for options
    const responseOptionAsked = await axios.get(`/api/question/options_asked`);
    hasAskedOptions.value = !!responseOptionAsked.data.options_asked;
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
        <AnswerForm @new-question="fetchNewQuestion" :hasAskedOptions="hasAskedOptions"/>
        <LeaderBoard :id_category="Number(id_category)"/>
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