/**
 * Client HTTP Axios pour l'API Django REST
 * - Base URL configurable via variable d'environnement
 * - Intercepteur : injecte automatiquement le token JWT dans chaque requête
 * - Intercepteur : gère le refresh automatique du token expiré (401)
 * - Intercepteur : redirige vers /login si le refresh échoue
 */

import axios from 'axios'
import router from '../router'

// ── Instance Axios principale ──────────────────────────────────────
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
  },
})


// ── Intercepteur REQUEST : injecter le token JWT ───────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)


// ── Intercepteur RESPONSE : gérer les erreurs 401 ─────────────────
let isRefreshing = false
let failedQueue  = []  // Requêtes en attente pendant le refresh

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error)
    else       prom.resolve(token)
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config

    // Si 401 et ce n'est pas déjà une tentative de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Mettre la requête en file d'attente
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }).catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem('refresh_token')

      if (!refreshToken) {
        // Pas de refresh token → déconnexion
        _logout()
        return Promise.reject(error)
      }

      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/token/refresh/`,
          { refresh: refreshToken }
        )

        const newAccess = data.access
        localStorage.setItem('access_token', newAccess)

        processQueue(null, newAccess)
        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        return api(originalRequest)

      } catch (refreshError) {
        processQueue(refreshError, null)
        _logout()
        return Promise.reject(refreshError)

      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

function _logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push({ name: 'login' })
}


// ── Endpoints nommés ───────────────────────────────────────────────
export const authAPI = {
  login:   (data)       => axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/token/`, data),
  refresh: (data)       => axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/token/refresh/`, data),
  register:(data)       => api.post('/register/', data),
  profile: ()           => api.get('/profile/'),
  updateProfile:(data)  => api.put('/profile/', data),
}

export const declarationsAPI = {
  list:           (params) => api.get('/declarations/', { params }),
  detail:         (id)     => api.get(`/declarations/${id}/`),
  create:         (data)   => api.post('/declarations/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }  // Pour l'upload photo
  }),
  update:         (id, data)   => api.patch(`/declarations/${id}/`, data),
  delete:         (id)         => api.delete(`/declarations/${id}/`),
  myDeclarations: ()           => api.get('/declarations/mes_declarations/'),
  pertes:         ()           => api.get('/declarations/pertes/'),
  trouvailles:    ()           => api.get('/declarations/trouvailles/'),
  rechercher:     (data)       => api.post('/declarations/rechercher/', data),
  changerStatut:  (id, data)   => api.patch(`/declarations/${id}/changer_statut/`, data),
  downloadPDF:    (id)         => api.get(`/declarations/${id}/telecharger_recepisse/`, {
    responseType: 'blob'
  }),
}

export const categoriesAPI = {
  list:   () => api.get('/categories/'),
  detail: (id) => api.get(`/categories/${id}/`),
}

export const notificationsAPI = {
  list:         ()   => api.get('/notifications/'),
  nonLues:      ()   => api.get('/notifications/non_lues/'),
  marquerLue:   (id) => api.post(`/notifications/${id}/marquer_lue/`),
  toutMarquer:  ()   => api.post('/notifications/tout_marquer_lues/'),
}

export const statsAPI = {
  get: () => api.get('/statistiques/'),
}

export default api