<template>
  <header id="header">
    <v-row class="d-flex justify-center align-center px-5">
      <v-col class="d-flex justify-center pa-0" cols="3">
        <div class="header__logo">
          <img src="../assets/img/logo.svg" alt="logo RosBank">
        </div>
      </v-col>
      <v-col class="d-flex justify-center pa-0" cols="6">
        <div class="header__title">
          <span>Отправка сообщения свободного формата</span>
        </div>
      </v-col>
      <v-col class="d-flex justify-center pa-0" cols="3">
        <v-select
          :items="users"
          color="#e60028"
          label="Выбрать пресет пользователя"
          item-text="title"
          item-value="id"
          return-object
          no-data-text="Пресет не загружен"
          :loading="loading"
          flat
          @change="pickedPreset"
        />
      </v-col>
    </v-row>
  </header>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */
  import axios from 'axios'

  export default {
    name: 'cHeader',
    components: {},
    data() {
      return {}
    },
    props: {
      loading: Boolean
    },
    computed: {
      users() {
        return this.$store.getters.getUsers
      }
    },
    watch: {},
    created() {},
    mounted() {},
    methods: {
      async pickedPreset(item) {
        this.$store.dispatch("PresetUser", await this.sendIdUser(item.id))
      },
      sendIdUser(id) {
        return new Promise((res, rej) => {
          axios({
            method: 'get',
            url: `http://localhost:5000/get_user/${id}`
          })
            .then(result => {
              res(result.data)
            })
            .catch(err => {
              console.log('Ошибка:')
              console.log(err)
              rej(err)
            })
        })
      }
    }
  }
</script>