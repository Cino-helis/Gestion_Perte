/**
 * Store Pinia — Authentification
 * Gère : login, logout, register, profil, état de connexion
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../services/api'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {

  // ── State ──────────────────────────────────────────────────────
  const user         = ref(null)
  const accessToken  = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const loading      = ref(false)
  const error        = ref(null)

  // ── Getters ────────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin  = computed(() => user.value?.role === 'admin')
  const isPolice = computed(() => user.value?.role === 'police')
  const isStaff  = computed(() => ['admin', 'police'].includes(user.value?.role))
  const userRole = computed(() => user.value?.role || 'citoyen')

  // ── Actions ────────────────────────────────────────────────────

  /** Connexion utilisateur */
  async function login(credentials) {
    loading.value = true
    error.value   = null

    try {
      const { data } = await authAPI.login(credentials)

      // Stocker les tokens
      accessToken.value  = data.access
      refreshToken.value = data.refresh
      localStorage.setItem('access_token',  data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // Charger le profil
      await fetchProfile()

      // Redirection selon le rôle
      if (isStaff.value) {
        router.push({ name: 'dashboard' })
      } else {
        router.push({ name: 'mes-declarations' })
      }

      return { success: true }

    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Inscription */
  async function register(userData) {
    loading.value = true
    error.value   = null

    try {
      await authAPI.register(userData)
      // Connexion automatique après inscription
      return await login({
        username: userData.username,
        password: userData.password,
      })
    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Récupération du profil utilisateur */
  async function fetchProfile() {
    try {
      const { data } = await authAPI.profile()
      user.value = data
    } catch (err) {
      // Token invalide → déconnexion
      if (err.response?.status === 401) logout()
    }
  }

  /** Mise à jour du profil */
  async function updateProfile(profileData) {
    loading.value = true
    error.value   = null
    try {
      const { data } = await authAPI.updateProfile(profileData)
      user.value = data
      return { success: true }
    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Déconnexion */
  function logout() {
    user.value         = null
    accessToken.value  = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push({ name: 'home' })
  }

  /** Initialisation au démarrage (si token présent en localStorage) */
  async function init() {
    if (accessToken.value) {
      await fetchProfile()
    }
  }

  // ── Helper privé ───────────────────────────────────────────────
  function _parseError(err) {
    if (!err.response) return 'Erreur réseau. Vérifiez votre connexion.'
    const data = err.response.data
    if (typeof data === 'string')  return data
    if (data?.detail)              return data.detail
    if (data?.non_field_errors)    return data.non_field_errors[0]
    // Erreurs de champs : retourner la première
    const firstField = Object.keys(data)[0]
    if (firstField) return `${firstField}: ${data[firstField][0]}`
    return 'Une erreur est survenue.'
  }

  return {
    // State
    user, accessToken, refreshToken, loading, error,
    // Getters
    isAuthenticated, isAdmin, isPolice, isStaff, userRole,
    // Actions
    login, register, logout, fetchProfile, updateProfile, init,
  }
})