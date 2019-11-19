/* eslint-disable */
import axios from 'axios'

const apiUrl = '/api'

export default {
    searchMovies(params) {
        return axios.get(`${apiUrl}/movies`, {
            params
        })
    },
    getMovies_homepage() {
        return axios.get(`${apiUrl}/movies/homepage`)
    },
    getMovies_homepage_itembased(id) {
        return axios.get(`${apiUrl}/subscription/itembasedmovies2/${id}`)
    },
    getMovies_homepage_userbased(params) {
        return axios.post(`${apiUrl}/subscription/userbasedmovies/${params.id}`, { resemble_users: params.resemble_users })
    },
    searchGenre(params) {
        // movie search by genre
        return axios.get(`${apiUrl}/genres/`, {
            params,
        })
    },
    searchUsers(params) {
        return axios.get(`${apiUrl}/users/`, {
            params,
        })
    },
    searchAges(params) {
        return axios.get(`${apiUrl}/ages/`, {
            params,
        })
    },
    searchOccupations(params) {
        return axios.get(`${apiUrl}/occupations/`, {
            params,
        })
    },
    searchGenders(params) {
        return axios.get(`${apiUrl}/genders/`, {
            params,
        })
    }
}