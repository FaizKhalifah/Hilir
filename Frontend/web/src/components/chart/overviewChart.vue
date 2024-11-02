<template>
    <div class="chart-container">
        <canvas ref="overviewChart"></canvas>
    </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
    name: "OverviewChart",
    props: {
        childrenTotal: Number,
        exerciseTotal: Number,
        assesmentTotal: Number
    },
    data() {
        return {
            chartInstance: null
        };
    },
    mounted() {
        this.renderChart();
    },
    methods: {
    renderChart() {
        this.$nextTick(() => {
            const ctx = this.$refs.overviewChart?.getContext('2d');
            
            if (!ctx) {
                console.error("Failed to get 2D context");
                return;
            }

            // Hapus instance chart sebelumnya jika ada
            if (this.chartInstance) {
                this.chartInstance.destroy();
            }

            // Membuat instance chart baru
            this.chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Children', 'Exercises', 'Assessments'],
                    datasets: [{
                        label: 'Total Count',
                        data: [this.childrenTotal, this.exerciseTotal, this.assesmentTotal],
                        backgroundColor: ['#4caf50', '#2196f3', '#ff9800'],
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
    }
},
    watch: {
        // Watch for prop changes and re-render chart
        childrenTotal() { this.renderChart(); },
        exerciseTotal() { this.renderChart(); },
        assesmentTotal() { this.renderChart(); }
    },
    beforeUnmount() {
        // Destroy the chart instance when the component is unmounted to free resources
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }
    }
};
</script>

<style scoped>
.chart-container {
    max-width: 600px;
    margin: 0 auto;
}
</style>
