import Vue from 'vue';
import Vuex from 'vuex';

import { LightUser, BREAK_POINT_FOR_ADVANCED_SEARCH } from "./constants";
import agent from "./agent";


Vue.use(Vuex);

export default new Vuex.Store({

    state: {
        token: localStorage.getItem('token'),
        currentUser: null,
        isAuthenticated: false,
        categories: [],
        isMobileMenuOpened: false,
        isExtendedSearchSideBarOpened: false,
        isSearchBoxOpened: false,
        isSearchResultsOpened: false,
        isFirstLogin: false,
        advancedSearchInProcess: true,
        fbUser: null,
        windowWidth: window.innerWidth
    },

    mutations: {

        updateToken(state, newToken) {
            localStorage.setItem('token', newToken);
            state.token = newToken;
            state.isAuthenticated = true;
        },
        removeToken(state) {
            localStorage.removeItem('token');
            state.token = null;
            state.isAuthenticated = false;
        },

        setCurrentUser(state, user) {
            state.currentUser = new LightUser(user);
            state.isAuthenticated = true;
        },
        removeCurrentUser(state) {
            state.currentUser = null;
        },
        setCategories(state, categories) {
            state.categories = categories;
        },
        setMobileMenuOpened(state, isOpened) {
            state.isMobileMenuOpened = isOpened;
            if (state.isExtendedSearchSideBarOpened || isOpened) {
                document.body.style.overflowY = 'hidden';
            } else {
                document.body.style.overflowY = 'auto';
            }
        },
        setExtendedSearchSideBarOpened(state, isOpened = false) {
            state.isExtendedSearchSideBarOpened = (typeof isOpened === 'boolean') ? isOpened : false;

            if (state.windowWidth < BREAK_POINT_FOR_ADVANCED_SEARCH) {
                state.isSearchBoxOpened = !state.isSearchResultsOpened;
            } else {
                state.isSearchBoxOpened = true;
            }

            // document.body.style.overflowY = state.isExtendedSearchSideBarOpened ? 'hidden' : 'auto';
            if (state.isExtendedSearchSideBarOpened) {
                document.body.style.overflowY = 'hidden';
            } else {
                document.body.style.overflowY = 'auto';
                state.isSearchBoxOpened = false;
                state.isSearchResultsOpened = false;
            }
        },
        setSearchBoxOpened(state, isOpened = false) {
            state.isSearchBoxOpened = isOpened;
        },
        setSearchResultsOpened(state, isOpened = false) {
            if (this.windowWidth < BREAK_POINT_FOR_ADVANCED_SEARCH) {
                state.isSearchBoxOpened = false;
            }
            state.isSearchResultsOpened = isOpened;
        },
        setSearchProcess(state, value) {
            state.advancedSearchInProcess = value;
        },
        setStateOfFirstLogin(state, isFirst) {
            state.isFirstLogin = isFirst;
        },
        setFbUser(state, user) {
            state.fbUser = user;
        },
        removeFbUser(state) {
            state.fbUser = null;
        },
        setWindowWidth(state, width) {
            state.windowWidth = width;
        }
    },

    actions: {
        login({ commit }, payload) {
            commit('updateToken', payload.token);
            commit('setCurrentUser', payload.user);
        },
        purgeAuth({ commit }, removeToken=true) {
            if (removeToken) {
                commit('removeToken');
            }
            commit('removeCurrentUser');
        },
        refreshUser({ commit }, payload) {
            commit('setCurrentUser', payload);
        },
        getCategories({ commit }) {
            agent.Timeline.categories().then(res => {
                commit('setCategories', res.data)
            })
        },
        fbAuth({ commit }, user) {
            commit('setFbUser', user);
        },
        removeFbUser({ commit }) {
            commit('removeFbUser');
        }
    },

    getters: {
        filterSubcategories: state => name => (
            state.categories.map(
                c => ({
                    ...c,
                    subcategories: c.subcategories.filter(s => s.name.toLowerCase().includes(name.toLowerCase()))
                })
            )
        )
    }
});