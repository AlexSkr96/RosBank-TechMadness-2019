<template>
  <v-col class="d-flex justify-center align-center flex-wrap" cols="3">
    <div class="seporator" v-if="pushup.length === 0" />
    <v-row v-else class="d-flex justify-center align-center">
      <transition-group name="slide-fade" tag="div">
      <v-alert 
        width="256"
        class="alert my-2"
        color="#dfd7d5"
        v-for="item in pushup" 
        :key="item.id"
      >
        <h2 class="subtitle-1">У вас незавершенное обращение #{{ item.id }}</h2>
        <h3 class="subtitle-2">Вас интересует тема: {{ item.title }}?</h3>        
        <v-row
          class="d-flex justify-center align-center"
          no-gutters
        >
          <v-hover 
            v-slot:default="{ hover }"
            open-delay="150"
          >
            <v-btn
              
              text
              :class="[hover ? 'hover success' : '']"
              width="105"
              @click="successPushup(item.id)"
            >
              Да
            </v-btn>
          </v-hover>
          <v-divider
            class="vertical-seporator"
            color="#fff"
            inset
            vertical
          />
          <v-hover 
            v-slot:default="{ hover }"
            open-delay="150"
          >
            <v-btn
              
              text
              :class="[hover ? 'hover error' : '']"
              width="105"
              @click="removePushup(item.id)"
            >
              Нет
            </v-btn>
          </v-hover>
        </v-row>
      </v-alert>
      </transition-group>
    </v-row>  
  </v-col>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */

  export default {
    name: 'cPushupMessage',
    components: {},
    data() {
      return {
        pushup: []
      }
    },
    props: {},
    computed: {
      presetUser() {
        return this.$store.getters.getPresetUser
      }
    },
    watch: {},
    created() {
      setTimeout(() => {
        this.refreshPushupMessage()
      }, 30000)
    },
    mounted() {},
    methods: {
      successPushup(id) {
        this.pushup = this.pushup.filter(item => {
          return id != item.id
        })
      },
      removePushup(id) {
        this.pushup = this.pushup.filter(item => {
          return id != item.id
        })
      },
      refreshPushupMessage() {
        if (this.pushup.length === 0) {
          if (this.presetUser.operations.length != 0) {
            this.presetUser.operations.forEach(item => {
              if (item.active === true) this.pushup.push({id: item.id, title: item.tags[0]})
            })
          }
        }
      }
    }
  }
</script>
<style scoped lang="sass">
  .alert
    box-shadow: 0 4px 2.5px #807d7d
  .vertical-seporator
    padding: 0 1px
    margin: 0
  .subtitle-1
    font-weight: 700
  .subtitle-2
    font-weight: 400
  .subtitle-1, .subtitle-2
    color: #fff
    text-align: center
    margin: 0 0 1rem
  .v-btn
    color: #fff
    caret-color: rgb(223, 215, 213)
  .v-btn.hover.error
    color: #fff
    caret-color: rgb(230, 0, 40)
  .v-btn.hover.success
    color: #fff
    caret-color: #4caf50
  .seporator
    min-width: 256px
  .slide-fade-enter-active
    transition: all .7s ease
  .slide-fade-leave-active
    transition: all .7s cubic-bezier(1.0, 0.5, 0.8, 1.0)
  .slide-fade-enter, .slide-fade-leave-to
    transform: translateY(-10px)
    opacity: 0
</style>
