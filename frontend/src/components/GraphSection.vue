<script setup>
import { ref, computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Tooltip, PointElement, LineElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Tooltip, PointElement, LineElement, CategoryScale, LinearScale)

const data = ref([])
const chartData = computed(() => {
    let val = {
        labels: data.value,
        datasets: [
            {
                backgroundColor: 'rgba(255, 0, 0, 1)',
                borderColor: 'rgba(255, 0, 0, 1)',
                data: data.value
            }
        ]
    };
    return val;
});

const addData = (valueToAdd) => {
    // pushing the new value to the data array (reactivity is handled by Vue)
    data.value = [...data.value, valueToAdd]
}
// expose because addData is called by the parent component
defineExpose({
    addData
})

const chartOptions = ref({
    scales: {
        responsive: true,
        maintainAspectRation: false,
        x: {
            display: false,
        },
        y: {
            display: true,
            title: {
                display: true,
                text: 'IQ Score',
                color: 'darkgray'
            },
            min: 0,
            max: 250
        }
    }
});

</script>

<template>
    <h2 class="title">Progression</h2>
    <div class="graph-container">
        <Line :data="chartData" :options="chartOptions" />
    </div>
</template>

<style scoped style="scss">
.graph-container {
    margin-bottom: 1.3rem;
    padding: 1rem;
    border-radius: 20px;
    background-color: #F6F6F6;
}
</style>
