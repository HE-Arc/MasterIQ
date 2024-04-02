<script setup>
import { useRoute } from 'vue-router';
import axios from 'axios';
import { defineEmits, onMounted, ref } from 'vue';

// default variables
const route = useRoute();
const id_category = route.params.id_category;

// variables specific to this component
const emit = defineEmits(['newQuestion'])
const answer_sent = ref(false);
const show_text_form = ref(true);
const answer_text = ref("");

const options = ref([]);

const response_to_answer = ref(null);

const submitAnswerText = async () => {
    const response = await axios.post(`/api/question/answer_text/`, {
        answer: answer_text.value,
    });
    response_to_answer.value = response.data;
    answer_sent.value = true;
}

const submitAnswerOption = async (key) => {
    const response = await axios.post(`/api/question/answer_option/`, {
        answer: key,
    });
    response_to_answer.value = response.data;
    answer_sent.value = true;
}

const fetchOptions = async () => {
    show_text_form.value = false;
    const response = await axios.get(`/api/question/options/`, {
    });
    options.value = response.data.options;
}

const hasAskedOptions = async () => {
    const response = await axios.get(`/api/question/has_asked_options/`); // TODO
    return !!response.data.has_asked_options; // TODO
}

const newQuestion = () => {
    answer_sent.value = false;
    show_text_form.value = true;
    answer_text.value = "";
    emit('newQuestion');
}

onMounted(() => {
    // ask backend if the user has already ask options in this category
    // if so, show the options form
    /*
    if (hasAskedOptions()) {
        fetchOptions();
        show_text_form.value = false;
    }*/
    // if not, show the text form (default value is true)

});
</script>

<template>
    <div v-if="show_text_form">
        <div v-if="!answer_sent" class="answer-text box">
            <span>Answer directly</span>
            <input type="text" v-model="answer_text" />
            <button class="btn" id="submit-answer-text" v-if="answer_text != ''" @click="submitAnswerText">Submit this
                answer</button>
            <span>or</span>
            <button class="btn" @click="fetchOptions">Ask options</button>
        </div>
        <div v-else>
            <p v-if="response_to_answer.user_is_correct" class="right-answer info-answer box">
                Good job! {{ response_to_answer.right_answer }} was the right answer!
            </p>
            <p v-else class="wrong-answer info-answer box">
                Unfortunately, your answer "{{ response_to_answer.answer_sent }}" was wrong. The correct answer was "{{
        response_to_answer.right_answer }}".
            </p>
            <button class="btn" @click="newQuestion">Next question</button>
        </div>
    </div>
    <div v-else class="answer-options">
        <div v-if="answer_sent">
            <p v-if="response_to_answer.user_is_correct" class="right-answer info-answer box">Good job, "{{
        response_to_answer.right_answer }}"
                was the right answer!</p>
            <p v-else class="wrong-answer info-answer box">
                Unfortunately, your answer "{{ response_to_answer.answer_sent }}" was wrong. The correct answer was "{{
        response_to_answer.right_answer }}"</p>
        
            <button class="btn" @click="newQuestion">Next question</button>
        </div>
        <div v-else class="box">
            <button v-for="(option, key, index) in options" :key="key" class="btn option"
                @click="submitAnswerOption(key)">{{ index + 1 }}. {{ option }}</button>
        </div>
    </div>
</template>

<style scoped style="scss">
.answer-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

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

.answer-options {
    .option {
        width: 100%;
        margin-bottom: 1rem;
        text-align: left;

        &:last-child {
            margin-bottom: 0;
        }
    }
}

.info-answer {
    font-weight: bold;
    padding: 1rem 2rem;
    margin-bottom: 1.3rem;
}

.right-answer {
    background-color: var(--color-background-right);
    color: var(--color-right);
}

.wrong-answer {
    background-color: var(--color-background-wrong);
    color: var(--color-wrong);
}
</style>