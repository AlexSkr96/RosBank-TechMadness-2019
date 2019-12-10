import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    users: [],
    presetUser: {},
    allOperations: [{
      id: 0,
      name: 'Кредитование'
    }, {
      id: 1,
      name: 'Депозиты'
    }, {
      id: 2,
      name: 'Валютный контроль'
    }, {
      id: 3,
      name: 'Карты'
    }, {
      id: 4,
      name: 'ЗП'
    }, {
      id: 5,
      name: 'ВЖП'
    }, {
      id: 6,
      name: 'Техническая поддержка'
    }]
  },
  getters: {
    getUsers: store => store.users,
    getPresetUser: store => store.presetUser,
    getAllOperations: store => store.allOperations
  },
  mutations: {
    Users(state, payload) {
      state.users = payload
    },
    PresetUser(state, payload) {
      state.presetUser = payload
    },
    AllOperations(state, payload) {
      state.allOperations = payload
    }
  },
  actions: {
    Users(context, payload) {
      context.commit('Users', payload)
    },
    PresetUser(context, payload) {
      context.commit('PresetUser', payload)
    },
    AllOperations(context, payload) {
      context.commit('AllOperations', payload)
    }
  }
})
