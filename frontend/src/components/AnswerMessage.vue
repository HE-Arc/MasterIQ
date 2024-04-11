<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    response_to_answer: {
        type: Object,
        required: true,
    }
})
</script>

<template>
    <div>
        <p v-if="props.response_to_answer.user_is_correct && props.response_to_answer.right_answer == props.response_to_answer.answer_sent"
            class="right-answer info-answer box">
            Good job! "{{ props.response_to_answer.right_answer }}" was the right answer!
        </p>
        <p v-else-if="props.response_to_answer.user_is_correct" class="right-answer info-answer box">
            Good job! You answered "{{ props.response_to_answer.answer_sent }}", and "{{ props.response_to_answer.right_answer }}" was the correct answer!
        </p>
        <p v-else class="wrong-answer info-answer box">
            Unfortunately, your answer "{{ props.response_to_answer.answer_sent }}" was wrong. The correct answer was
            "{{
            props.response_to_answer.right_answer }}".
        </p>
    </div>
</template>

<style scoped style="scss">
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