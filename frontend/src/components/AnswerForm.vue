<script setup>
import APIClient from '@/api_client';
import { defineEmits, onMounted, ref, defineProps, watch } from 'vue';
import AnswerMessage from '@/components/AnswerMessage.vue';
import {useRoute} from "vue-router";

// variables specific to this component
const route = useRoute()
const id_category = route.params.id_category;
const emit = defineEmits(['newQuestion', 'updateUserIq'])
const answer_sent = ref(false);
const show_text_form = ref(true);
const answer_text = ref("");

const options = ref([]);

const response_to_answer = ref(null);

const props = defineProps({
    hasAskedOptions: {
        type: Boolean,
        required: true,
    }
})

const submitAnswerText = async () => {
    response_to_answer.value = await APIClient.postAnswerText(answer_text.value, id_category);
    answer_sent.value = true;
    emit('updateUserIq');
}

const submitAnswerOption = async (id) => {
    response_to_answer.value = await APIClient.postAnswerOption(id, id_category);
    answer_sent.value = true;
    emit('updateUserIq');
}

const fetchOptions = async () => {
    show_text_form.value = false;
    options.value = await APIClient.getOptions(id_category);
}

const newQuestion = () => {
    answer_sent.value = false;
    show_text_form.value = true;
    answer_text.value = "";
    emit('newQuestion');
}

const displayOptionsAsked = () => {
    if (props.hasAskedOptions) {
        fetchOptions();
        show_text_form.value = false;
    }
}

onMounted(() => {
    displayOptionsAsked();
});

watch(() => props.hasAskedOptions, () => {
    displayOptionsAsked();
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
            <AnswerMessage :response_to_answer="response_to_answer" />
            <button class="btn" @click="newQuestion">Next question</button>
        </div>
    </div>
    <div v-else class="answer-options">
        <div v-if="answer_sent">
            <AnswerMessage :response_to_answer="response_to_answer" />
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
</style>