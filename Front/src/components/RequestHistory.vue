<template>
  <v-col class="d-flex" cols="6">
    <v-card
      width="100%"
      class="mx-auto pa-5"
    >
      <v-data-table
        v-if="presetUser.operations.length != 0"
        :headers="headers"
        :items="desserts"
        :items-per-page="5"
        class="elevation-1"
      />
      <h2 v-else>У вас еще нет запросов</h2>
    </v-card>
  </v-col>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */

  export default {
    name: 'cRequestHistory',
    components: {},
    data() {
      return {
        headers: [{
          text: 'Номер заявки', 
          value: 'number' 
        }, {
          text: 'Дата', 
          value: 'date' 
        }, {
          text: 'ФИО', 
          value: 'name' 
        }, {
          text: 'Тема', 
          value: 'topic' 
        }, {
          text: 'Тип операций', 
          sortable: false, 
          value: 'typeOperations' 
        }, {
          text: 'Статус операции',
          value: 'statusOperations' 
        }],
        desserts: []
      }
    },
    props: {},
    computed: {
      users() {
        return this.$store.getters.getUsers
      },
      presetUser() {
        return this.$store.getters.getPresetUser
      }
    },
    watch: {},
    created() {},
    mounted() {
      console.log(this.presetUser.operations)
      this.presetUser.operations.forEach(item => {
        this.desserts.push({
          number: item.id,
          date: this.formatDate(item.date),
          name: this.getInfoUsers(item.user_id),
          topic: item.topic,
          typeOperations: item.tags,
          statusOperations: item.active === true ? 'Незавершена' : 'Завершена'
        })
      })
    },
    methods: {
      getInfoUsers(userID) {
        let user = {}

        user = this.users.filter(item => {
          return userID === item.id
        })
        console.log(user)

        return user[0].name
      },
      formatDate(sourceDate) {
        const date = new Date(sourceDate)
        let dd = date.getDate(),
            mm = date.getMonth() + 1,
            yy = date.getFullYear()

        if (dd < 10) dd = '0' + dd
        if (mm < 10) mm = '0' + mm
        
        return dd + '.' + mm + '.' + yy
      }
    }
  }
</script>