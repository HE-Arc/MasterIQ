<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    label: {
        type: String,
        required: true,
    },
    hasLabel: {
        type: Boolean,
        default: true,
        required: false,
    },
    modelValue: {
        type: String,
        required: true,
    },
    type: {
        type: String,
        default: 'text',
        required: false,
    },
    required: {
        type: Boolean,
        default: false,
        required: false,
    },
});

const name = computed(() => props.label.toLowerCase());

const emit = defineEmits(['update:modelValue', 'change']);

// Peut ajouter la validation ici
const onInput = (event) => {
    emit('update:modelValue', event.target.value);
    emit('input', event.target.value);
};

const onChange = (event) => {
    emit('change', event.target.value);
};
</script>

<template>
    <div class="input-container">
        <label v-if="hasLabel" :for="name">{{ label }}<span v-if="props.required">*</span></label>
        <input :type="type" :id="name" :name="name" :value="modelValue" @input="onInput" @change="onChange" maxlength="25" :required="required"/>
    </div>
</template>

<style scoped>
input 
{
    display: block; 
    width: 100%;
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    border-color: var(--color-border);
    border-style: solid;
}
</style>