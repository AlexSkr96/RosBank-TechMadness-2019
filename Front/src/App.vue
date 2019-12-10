<template>
  <v-app id="app">
    <v-content>
      <Header :loading="loading" />
      <v-container v-show="show" id="main" fluid>
        <v-row class="d-flex justify-center align-start">
          <MenuActions @selectMenu="selectMenu" />
          <Form v-if="selectedMenu.title === 'Форма'" />
          <RequestHistory v-else />
          <PushupMessage />
        </v-row>
      </v-container>
      <Footer />
    </v-content>
  </v-app>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */
import Header from './components/Header'
import MenuActions from './components/MenuActions'
import Form from './components/Form'
import RequestHistory from './components/RequestHistory'
import PushupMessage from './components/PushupMessage'
import Footer from './components/Footer'
import axios from 'axios'

  export default {
    name: 'cApp',
    components: {
      Header,
      MenuActions,
      Form,
      RequestHistory,
      PushupMessage,
      Footer
    },
    data() {
      return {
        loading: false,
        show: false,
        selectedMenu: {
          id: 0,
          title: 'Форма',
          icon: 'mdi-book-information-variant'
        }
      }
    },
    props: {},
    computed: {
      presetUser() {
        return this.$store.getters.getPresetUser
      }
    },
    watch: {
      presetUser(v) {
        if (v != undefined) {
          this.show = true
        } else {
          this.show = false
        }
      }
    },
    async created() {
      this.$store.dispatch("Users", await this.getUsers())
    },
    mounted() {},
    methods: {
      getUsers() {
        this.loading = true
        return new Promise((res, rej) => {
          axios({
            method: 'get',
            url: `http://localhost:5000/get_users`
          })
            .then(result => {
              this.loading = false
              res(result.data)
            })
            .catch(err => {
              console.log('Ошибка:')
              console.log(err)
              rej(err)
            })
        })
      },
      selectMenu(data) {
        this.selectedMenu = data
      }
    }
  }
</script>
