<template>
    <Bar
        id="my-chart-id"
        :options="chartOptions"
        :data="chartData"
    />
</template>

<script>
    import { Bar } from 'vue-chartjs'
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

    export default {
        name: 'BarChart',
        components: { Bar },
        data() {
            return {
                chartData: {
                    labels: [ 'normal', 'pyriform', 'amorphous', 'tapered' ],
                    datasets: [ { label: "Répartition des classes (%)", data: [40, 20, 40, 20], backgroundColor: "lightblue" } ]
                },
                chartOptions: {
                    responsive: true
                }
            }
        }
    }
</script>
