/* eslint-disable */
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueSession from 'vue-session'
import HomePage from '../components/pages/HomePage'
import MovieSearchPage from '../components/pages/MovieSearchPage'
import MovieDetailPage from '../components/pages/MovieDetailPage'
import UserSearchPage from '../components/pages/UserSearchPage'
import UserDetailPage from '../components/pages/UserDetailPage'
import SignUpPage from '../components/pages/SignUpPage'
import SignInPage from '../components/pages/SignInPage'
import AdminPage from '../components/pages/AdminPage'
import MyPage from '../components/pages/MyPage'
import MovieChoicePage from '../components/pages/MovieChoicePage'
import SupportPage from '../components/pages/SupportPage'

Vue.use(VueRouter)
Vue.use(VueSession)

const router = new VueRouter({
    mode: 'history',
    routes: [
        { path: '/', component: HomePage, name: 'home' },
        { path: '/movies/search', component: MovieSearchPage, name: 'movie-search' },
        { path: '/movies/detail/:id', component: MovieDetailPage, name: 'movie-detail', props: true },
        { path: '/users/search', component: UserSearchPage, name: 'user-search' },
        { path: '/users/detail/:id', component: UserDetailPage, name: 'user-detail', props: true },
        { path: '/users/signup', component: SignUpPage, name: 'sign-up' },
        { path: '/users/signin', component: SignInPage, name: 'sign-in' },
        { path: '/admin/', component: AdminPage, name: 'admin-page' },
        { path: '/mypage/', component: MyPage, name: 'my-page' },
        { path: '/choices/', component: MovieChoicePage, name: 'movie-choice' },
        { path: '/support/', component: SupportPage, name: 'support-page' },
    ],
    scrollBehavior() {
        return { x: 0, y: 0 }
    },
})

export default router