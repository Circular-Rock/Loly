import {createStore} from 'vuex';

export default createStore({
    state: {
        username: ''
    },
    mutations: {
        SET_USERNAME(state, username) {
            state.username = username;
        }
    },
    actions: {
        setUsername({commit}, username) {
            commit('SET_USERNAME', username);
        }
    }
});
  