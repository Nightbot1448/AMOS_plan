import Vue from 'vue';
import Vuex from 'vuex'

Vue.use(Vuex)
export const store = new Vuex.Store({
    state: {
        variant: null,
        pa_points: null,  //planning area points
        p_points: null,  //planning points
        p_points_len: null,
        number_of_experiments: null,
        randomization: false,
    },
    mutations: {
        change_variant(state, new_variant) {
            state.variant = new_variant;
        },
        change_pa_points(state, new_pa_points) {
            state.pa_points = new_pa_points;
        },
        change_p_points(state, new_p_points) {
            state.p_points = new_p_points;
        },
        change_p_points_len(state, new_p_points_len) {
            state.p_points_len = new_p_points_len;
        },
        change_number_of_experiments(state, new_number_of_experiments) {
            state.number_of_experiments = new_number_of_experiments;
        },
        change_randomization(state, new_randomization) {
            state.randomization = new_randomization;
        },
    },
    getters: {
        variant(state) {
            return state.variant;
        },
        pa_points(state) {
            return state.pa_points
        },
        p_points(state) {
            return state.p_points
        },
        p_points_len(state) {
            return state.p_points_len
        },
        number_of_experiments(state) {
            return state.number_of_experiments
        },
        randomization(state) {
            return state.randomization
        },
    },
    actions: {
        changeVariant({ commit }, new_variant) {
            commit('change_variant', new_variant)
        },
        changePAPoints({ commit }, new_pa_points) {
            commit('change_pa_points', new_pa_points)
        },
        changePPoints({ commit }, new_p_points) {
            commit('change_p_points', new_p_points)
        },
        changePPointsLen({ commit }, new_p_points_len) {
            commit('change_p_points_len', new_p_points_len)
        },
        changeNExperiments({ commit }, new_number_of_experiments) {
            commit('change_number_of_experiments', new_number_of_experiments)
        },
        changeRandomization({ commit }, new_randomization) {
            commit('change_randomization', new_randomization)
        },
    }
})