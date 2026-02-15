/**
 * Client HTTP Axios — DéclaTogo
 */

import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
})

// ── Intercepteur REQUEST ──────────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// ── Intercepteur RESPONSE — refresh JWT ──────────────────────────
let isRefreshing = false
let failedQueue  = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  failedQueue = []
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const orig = error.config
    if (error.response?.status === 401 && !orig._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => failedQueue.push({ resolve, reject }))
          .then((token) => { orig.headers.Authorization = `Bearer ${token}`; return api(orig) })
          .catch((err) => Promise.reject(err))
      }
      orig._retry   = true
      isRefreshing  = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) { _logout(); return Promise.reject(error) }
      try {
        const base = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/'
        const { data } = await axios.post(`${base}token/refresh/`, { refresh })
        localStorage.setItem('access_token', data.access)
        processQueue(null, data.access)
        orig.headers.Authorization = `Bearer ${data.access}`
        return api(orig)
      } catch (e) {
        processQueue(e, null)
        _logout()
        return Promise.reject(e)
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

// ═════════════════════════════════════════════════════════════════
// Endpoints
// ═════════════════════════════════════════════════════════════════

export const authAPI = {
  login:         (d) => api.post('token/', d),
  refresh:       (d) => api.post('token/refresh/', d),
  register:      (d) => api.post('register/', d),
  profile:       ()  => api.get('profile/'),
  updateProfile: (d) => api.put('profile/', d),
}

export const declarationsAPI = {
  list:          (params)   => api.get('declarations/', { params }),
  detail:        (id)       => api.get(`declarations/${id}/`),
  create:        (data)     => api.post('declarations/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update:        (id, data) => api.patch(`declarations/${id}/`, data),
  /** Suppression définitive — admin uniquement */
  delete:        (id)       => api.delete(`declarations/${id}/`),
  myDeclarations:()         => api.get('declarations/mes_declarations/'),
  pertes:        ()         => api.get('declarations/pertes/'),
  trouvailles:   ()         => api.get('declarations/trouvailles/'),
  rechercher:    (data)     => api.post('declarations/rechercher/', data),
  changerStatut: (id, data) => api.patch(`declarations/${id}/changer_statut/`, data),
  downloadPDF:   (id)       => api.get(`declarations/${id}/telecharger_recepisse/`, {
    responseType: 'blob',
  }),
}

export const categoriesAPI = {
  list:   () => api.get('categories/'),
  detail: (id) => api.get(`categories/${id}/`),
}

export const notificationsAPI = {
  list:        ()   => api.get('notifications/'),
  nonLues:     ()   => api.get('notifications/non_lues/'),
  marquerLue:  (id) => api.post(`notifications/${id}/marquer_lue/`),
  toutMarquer: ()   => api.post('notifications/tout_marquer_lues/'),
}

export const statsAPI = {
  get: () => api.get('statistiques/'),
}

// ── Gestion agents (admin) ────────────────────────────────────────
export const agentsAPI = {
  list:   ()         => api.get('admin/agents/'),
  create: (data)     => api.post('admin/agents/', data),
  update: (id, data) => api.patch(`admin/agents/${id}/`, data),
  delete: (id)       => api.delete(`admin/agents/${id}/`),
}

// ── Gestion utilisateurs (admin) — NOUVEAU ───────────────────────
export const usersAPI = {
  /** Liste tous les utilisateurs (filtres : role, search) */
  list:   (params)   => api.get('admin/users/', { params }),
  /** Détail d'un utilisateur */
  detail: (id)       => api.get(`admin/users/${id}/`),
  /** Modifier (is_active, …) */
  update: (id, data) => api.patch(`admin/users/${id}/`, data),
  /** Suppression DÉFINITIVE */
  delete: (id)       => api.delete(`admin/users/${id}/`),
}

export default api