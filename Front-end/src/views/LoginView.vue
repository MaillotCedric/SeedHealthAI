<template>
  <div class="login">
    <Transition>
      <v-alert
        class="mb-2"
        :title="alert_title"
        :type="alert_type"
        :text="alert_text"
        v-if="show_alert"
      >
      </v-alert>
    </Transition>
    <v-form @submit.prevent="login_">
      <v-text-field clearable label="Username" v-model="username"> </v-text-field>
      <v-text-field clearable label="Password" type="password" v-model="password"> </v-text-field>
      <v-btn :loading="loading" type="submit" variant="outlined"> Login </v-btn>
    </v-form>
  </div>
</template>

<script lang="ts">
import * as tb from '../scripts/toolbox'
import axios from 'axios'

export default {
  data() {
    return {
      alert_text: '',
      alert_title: '',
      alert_type: undefined,
      loading: false,
      password: '',
      show_alert: false,
      username: ''
    }
  },
  methods: {
    login_() {
      let form_data = {
        username: this.username,
        password: this.password
      }

      this.loading = true

      axios
        .post('/api/token/', form_data)
        .then((response) => {
          // tb.print_(response.data)
          this.stop_loading()
          this.alert_text = 'Logged in'
          this.alert_title = 'Success'
          this.alert_type = 'success'
          this.display_alert()
        })
        .catch((error) => {
          // tb.print_(error.response.data)
          this.stop_loading()
          this.alert_text = 'Credentials error'
          this.alert_title = 'Error'
          this.alert_type = 'error'
          this.display_alert()
        })
    },
    display_alert() {
      this.show_alert = true
      setTimeout(() => (this.show_alert = false), 2000)
    },
    stop_loading() {
      this.loading = false
    }
  }
}
</script>

<style>
@media (min-width: 1024px) {
  /* .login {
            min-height: 100vh;
            display: flex;
            align-items: center;
        } */
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
