<script setup>
import { useRoute } from 'vue-router';
import axios from 'axios';
import { onMounted, ref } from 'vue';
// default variables
const route = useRoute();
const id_category = route.params.id_category;

// variables specific to this component
const answer_text = ref("");
const show_text = ref(true);

const submitAnswerText = async () => {
    const response = await axios.post(`/api/question/answer_text/`, {
        answer: answer_text.value,
    });
    console.log(response.data);
}

const fetchOptions = async () => {
    show_text.value = false;
    const response = await axios.get(`/api/question/options/`, {
    });
    console.log(response.data);
}

</script>

<template>
    <div v-if="show_text" class="answer-text box">
        <span>Answer directly</span>
        <input type="text" v-model="answer_text" />
        <button class="btn" id="submit-answer-text" v-if="answer_text != ''" @click="submitAnswerText">Submit this answer</button>
        <span>or</span>
        <button class="btn" @click="fetchOptions">Ask options</button>
    </div>
    <div v-else class="answer-options box">

    </div>
</template>

<style scoped style="scss">
.answer-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 20px;

    span {
        font-size: 0.9rem;
        margin-bottom: 10px;
        font-style: italic;
    }

    input {
        padding: 1rem 2rem;
        border-radius: 27px;
        cursor: pointer;
        transition: 0.4s;
        font-weight: bold;
        font-size: 1rem;
        color: var(--color-text);

    }

    #submit-answer-text {
        margin-top: 10px;
        margin-bottom: 10px;
    }
}
</style>