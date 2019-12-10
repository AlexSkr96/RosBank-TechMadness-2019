<template>
  <v-col v-if="showActions" class="d-flex" cols="3">
    <v-card
      width="256"
      class="mx-auto"
    >
      <v-navigation-drawer permanent>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              {{ presetUser.user.name }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ presetUser.user.comp }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          dense
          nav
        >
          <v-list-item
            v-for="item in actions"
            :key="item.title"
            link
            :class="[item.active === true ? 'active' : '']"
            @click="pickedMenu(item)"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-card>
  </v-col>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */

  export default {
    name: 'cMenuActions',
    components: {},
    data() {
      return {
        showActions: false,
        actions: [{
          id: 0,
          title: 'Форма',
          icon: 'mdi-book-information-variant',
          active: true
        }, {
          id: 1,
          title: 'История запросов',
          icon: 'mdi-message-text',
          active: false
        }]
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
          this.showActions = true
        } else {
          this.showActions = false
        }
      }
    },
    created() {},
    mounted() {},
    methods: {
      pickedMenu(item) {
        this.actions.forEach(action => {
          if (action.id === item.id)  {
            action.active = true
            this.$emit('selectMenu', action)
          } else {
            action.active = false
          }
        })
      }
    }
  }
</script>
<style scoped lang="sass">
  .active
    background-color: #e60028
    .v-icon, .v-list-item__title
      color: #fff
</style>