<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import AnswerForm from '@/components/AnswerForm.vue';
import LeaderBoard from '@/components/LeaderBoard.vue';
import CategorieBanner from '@/components/CategorieBanner.vue';
import GraphSection from '@/components/GraphSection.vue';
import APIClient from '@/api_client';

// default variables
const route = useRoute();
const id_category = route.params.id_category;

// variables specific to this component
const question = ref(null);
const hasAskedOptions = ref(false);
const disclaimer = ref(false);

const fetchNewQuestion = async () => {
    question.value = await APIClient.getNewQuestion(id_category);
    // wait for the question before checking if the user has asked for options
    hasAskedOptions.value = await APIClient.getIfOptionsAsked(id_category);
};

// Fetch user IQ and add it to the graph
const graphComponent = ref(null);
const fetchUserIQ = async () => {
    const userIq = await APIClient.getUserIQ(id_category);
    graphComponent.value.addData(userIq);
};

onMounted(() => {
    fetchNewQuestion();
    fetchUserIQ();

    // Check if URL is matching to community category
    if (route.params.id_category === '23') {
        disclaimer.value = true;
    }
});
</script>


<template>
    <main class="container">
        <p v-if="disclaimer" class="disclaimer">Please be aware that this category contains question added by
            the users, and is not moderated. <br>
            The questions and answers provided here may be inaccurate, misleading, offensive or not adapted for
            younger users.</p>
        <section class="quiz col-wrapper">
            <p class="info">Answer correctly to the question and earn as many IQs as possible!</p>
            <div class="empty-space"></div>
            <div>
                <h1 class="title">Question</h1>
                <p class="question box">{{ question }}</p>
                <AnswerForm @new-question="fetchNewQuestion" @update-user-iq="fetchUserIQ"
                    :hasAskedOptions="hasAskedOptions" />
            </div>
            <div>
                <CategorieBanner class="category-banner" :id_category="Number(id_category)" />
                <GraphSection ref="graphComponent" />
                <LeaderBoard :id_category="Number(id_category)" />
            </div>
        </section>
    </main>
</template>

<style scoped>

.quiz
{
    padding-bottom: 2rem;
}
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

.disclaimer {
    font-weight: bold;
    color: red;
    margin-top: 1rem;
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
