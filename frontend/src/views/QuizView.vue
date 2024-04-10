<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import AnswerForm from '@/components/AnswerForm.vue';
import LeaderBoard from '@/components/LeaderBoard.vue';
import CategorieBanner from '@/components/CategorieBanner.vue';
import APIClient from '@/api_client';

// default variables
const route = useRoute();
const id_category = route.params.id_category;

// variables specific to this component
const question = ref(null);
const hasAskedOptions = ref(false);

const fetchNewQuestion = async () => {
    question.value = await APIClient.getNewQuestion(id_category)

    // wait for the question before checking if the user has asked for options
    hasAskedOptions.value = await APIClient.getIfOptionsAsked();
}

onMounted(() => {
    fetchNewQuestion();
});

</script>

<template>
    <section class="quiz container col-wrapper">
        <p class="info">Answer correctly to the question and earn as many IQs as possible!</p>
        <div class="empty-space"></div>
        <div>
            <h1 class="title">Question</h1>
            <p class="question box">{{ question }}</p>
            <AnswerForm @new-question="fetchNewQuestion" :hasAskedOptions="hasAskedOptions" />
        </div>
        <div>
            <CategorieBanner class="category-banner" :id_category="Number(id_category)" />
            <LeaderBoard :id_category="Number(id_category)" />
        </div>

    </section>
</template>

<style scoped>
.title {
    text-align: center;
}

.question {
    text-align: center;
    margin-bottom: 1.3rem;
}

.category-banner {
    display: none;
}

@media (min-width: 1024px) {
    .col-wrapper {
        display: grid;
        grid-template-columns: .66fr .33fr;
        column-gap: 2rem;
    }

    .category-banner {
        display: block;
    }
}
</style>