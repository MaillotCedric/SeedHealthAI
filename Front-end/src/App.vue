<template>
  <v-container class="form-container">
    <v-row>
      <v-col sm="6">
        <v-form @submit.prevent="predict">
          <v-select
            clearable
            label="Season"
            :items="['summer', 'spring', 'fall', 'winter']"
            variant="underlined"
            v-model="season"
            :rules="selectRules"
          ></v-select>

          <v-text-field
            clearable
            label="Age"
            variant="underlined"
            v-model="age"
            single-line
            type="number"
            :rules="ageRules"
          />
          
          <v-switch
            label="Childish diseases"
            v-model="childishDiseases"
            true-value="yes"
            false-value="no"
            color="info"
          ></v-switch>

          <v-switch
            label="Accident or serious trauma"
            v-model="accident"
            true-value="yes"
            false-value="no"
            color="info"
          ></v-switch>

          <v-switch
            label="Surgical intervention"
            v-model="surgicalIntervention"
            true-value="yes"
            false-value="no"
            color="info"
          ></v-switch>

          <v-select
            clearable
            label="High fevers in the last year"
            :items="['no', 'less than 3 months ago', 'more than 3 months ago']"
            variant="underlined"
            v-model="fevers"
            :rules="selectRules"
          ></v-select>

          <v-select
            clearable
            label="Frequency of alcohol consumption"
            :items="['hardly ever or never', 'once a week', 'several times a week', 'every day', 'several times a day']"
            variant="underlined"
            v-model="alcohol"
            :rules="selectRules"
          ></v-select>

          <v-select
            clearable
            label="Smoking habit"
            :items="['never', 'occasional', 'daily']"
            variant="underlined"
            v-model="smoking"
            :rules="selectRules"
          ></v-select>

          <v-text-field
            clearable
            label="Number of hours spent sitting per day"
            variant="underlined"
            v-model="sittingHours"
            single-line
            type="number"
            :rules="hoursRules"
          />

          <v-btn :loading=loadingPredict type="submit" block class="mt-2">Predict</v-btn>
        </v-form>
      </v-col>
      <v-col sm="6">
        <v-alert
          class="mb-2 mt-2"
          title="Diagnosis"
          :type=typeDiagnosis
          :text=textDiagnosis
        >
        </v-alert>

        <v-divider class="mb-2"></v-divider>

        <Classifier
          v-if=showClassifier
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import * as tb from './scripts/toolbox'
  import axios from 'axios'
  import Classifier from './components/Classifier.vue'

  export default {
    components: {
      Classifier
    },
    data() {
      return {
        season: null,
        age: null,
        childishDiseases: "no",
        accident: "no",
        surgicalIntervention: "no",
        fevers: null,
        alcohol: null,
        smoking: null,
        sittingHours: null,
        loadingPredict: false,
        typeDiagnosis: "info",
        textDiagnosis: "Ici s'affichera la prédiction concernant le diagnostic",
        showClassifier: false,
        selectRules: [
          (value) => {
            if (value) return true

            return 'You must select a value'
          },
        ],
        ageRules: [
          (value) => {
            if (value && value > 0 && value < 130) return true

            return 'You must enter a valid age'
          },
        ],
        hoursRules: [
          (value) => {
            if (value && value >= 0 && value <= 24) return true

            return 'You must enter a valid number of hours'
          },
        ],
      }
    },
    methods: {
      formFilled() {
        return (
          this.season != null
          && this.age != null && this.age > 0 && this.age < 130
          && this.fevers != null
          && this.alcohol != null
          && this.smoking != null
          && this.sittingHours != null && this.sittingHours >=0 && this.sittingHours <= 24
        )
      },
      getPrediction(value) {
        return value == 0 ? "Normal" : "Altered"
      },
      predict() {
        let formData = {
          "Inputs": {
            "input1": [
              {
                "Season": this.season,
                "Age": this.age,
                "Childish diseases": this.childishDiseases,
                "Accident or serious trauma": this.accident,
                "Surgical intervention": this.surgicalIntervention,
                "High fevers in the last year": this.fevers,
                "Frequency of alcohol consumption": this.alcohol,
                "Smoking habit": this.smoking,
                "Number of hours spent sitting per day": this.sittingHours
              }
            ]
          },
          "GlobalParameters": {}
        }

        if (this.formFilled()) {
          this.loadingPredict = true

          axios
          .post('/api/predict/', formData)
          .then((response) => {
            let resultat = response.data.Results.WebServiceOutput0[0]
            let prediction = this.getPrediction(resultat.FertilityPrediction)

            this.loadingPredict = false
            this.textDiagnosis = prediction
            this.typeDiagnosis = prediction == "Normal" ? "success" : "error"
            this.showClassifier = prediction == "Normal" ? false : true
            tb.print_(response.data)
          })
          .catch((error) => {
            tb.print_(error.response.data)
          })
        }
      }
    }
  }
</script>

<style>
  @media (min-width: 1024px) {
    .form-container {
      margin: 0px !important;
      max-width: inherit !important;
      padding: 0px !important;
    }
  }
</style>
