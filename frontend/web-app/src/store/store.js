import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const store = new Vuex.Store({
    state: {
        meterData: [],
        error: ""
    },
    mutations: {
        ADD_METER_DATA(state, data) {
            state.meterData.push(data)
        },
        SET_ERROR(state, error) {
            state.error = error
        }
    },
    actions: {
        loadData ({commit}) {
            commit('SET_ERROR', '')
            axios
                .get(`${process.env.VUE_APP_API_URL}/meter-usage`)
                .then(response => response.data)
                .then(data => {
                    if ('data' in data) {
                        data.data.forEach(item => {
                            commit('ADD_METER_DATA', {
                                timestamp: item.timestamp * 1000, // Unix timestamp is different than Javascript's
                                value: item.value
                            })
                        })
                    }
                })
                .catch(error => {
                    commit('SET_ERROR', error)
                })
        }
    },
    getters: {
        meterData: state => state.meterData
    }
})
