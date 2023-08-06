<template>
    <h2 class="mb-2">Évaluation morphologique</h2>

    <v-file-input
        multiple
        label="Provide a dataset of sperm head shape images ..."
        @change="handleChange"
        @click:clear="btnUploadVisible = false"
    ></v-file-input>
    <v-btn
        type="submit"
        block class="mt-2 mb-10"
        v-if="btnUploadVisible"
        @click="analyser"
        :loading="loadingAnalyse">Analyser les images
    </v-btn>

    <v-divider class="mb-2"></v-divider>

    <Bar v-if="loaded" :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
    import * as tb from '../scripts/toolbox'
    import axios from 'axios'
    import { Bar } from 'vue-chartjs'
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

    export default {
        components: { Bar },
        computed: {
            chartData() {
                return {
                    labels: [ 'normal', 'pyriform', 'amorphous', 'tapered' ],
                    datasets: [ { label: "Répartition des classes (%)", data: [], backgroundColor: "lightblue" } ]
                }
            },
            chartOptions() {
                return {
                    responsive: true
                }
            }
        },
        data() {
            return {
                nbFilesUploaded: 0,
                files: null,
                btnUploadVisible: false,
                loadingAnalyse: false,
                loaded: false
            }
        },
        methods: {
            handleChange(event) {
                this.btnUploadVisible = true
                this.files = event.target.files
            },
            analyser() {
                this.loadingAnalyse = true
                this.uploadFiles()
            },
            uploadFiles() {
                const formData = new FormData()

                for (let index = 0; index < this.files.length; index++) {
                    const file = this.files[index];
                    
                    formData.append("file", file)
                    axios
                    .post("api/images/", formData)
                    .then(() => {
                        if (this.nbFilesUploaded === this.files.length - 1) {
                            this.classify()
                        }
                        this.nbFilesUploaded++
                    })
                    .catch(() => {
                        console.log("Upload failed");
                    });
                }
            },
            classify() {
                axios
                .get("api/classify/")
                .then((response) => {
                    let values: Array<number> = []

                    for (const key in response.data){
                        values.push(parseInt(response.data[key]))
                    }

                    this.chartData.datasets[0].data = values
                    this.loaded = true

                    this.loadingAnalyse = false
                })
                .catch(() => {
                    console.log("Classify failed");
                });
            }
        }
    }
</script>

<style>
    @media (min-width: 1024px) {}
</style>
  