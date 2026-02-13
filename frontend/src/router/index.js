/**
 * Vue Router — DéclaTogo
 * Lazy loading sur toutes les pages pour minimiser le bundle initial
 * Guards : redirige les non-connectés, protège les routes admin/police
 */

import { createRouter, createWebHistory } from 'vue-router'

// ── Routes (lazy-loaded) ───────────────────────────────────────────
const routes = [
  // Pages publiques
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'Accueil — DéclaTogo', public: true },
  },
  {
    path: '/rechercher',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
    meta: { title: 'Rechercher une pièce — DéclaTogo', public: true },
  },

  // Authentification
  {
    path: '/connexion',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { title: 'Connexion — DéclaTogo', public: true, guestOnly: true },
  },
  {
    path: '/inscription',
    name: 'register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { title: 'Inscription — DéclaTogo', public: true, guestOnly: true },
  },

  // Espace citoyen (authentifié)
  {
    path: '/mes-declarations',
    name: 'mes-declarations',
    component: () => import('../views/citizen/MyDeclarationsView.vue'),
    meta: { title: 'Mes déclarations — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/declarer',
    name: 'declare',
    component: () => import('../views/citizen/DeclareView.vue'),
    meta: { title: 'Déclarer — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/declarations/:id',
    name: 'declaration-detail',
    component: () => import('../views/citizen/DeclarationDetailView.vue'),
    meta: { title: 'Détail — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/profil',
    name: 'profile',
    component: () => import('../views/citizen/ProfileView.vue'),
    meta: { title: 'Mon profil — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: () => import('../views/citizen/NotificationsView.vue'),
    meta: { title: 'Notifications — DéclaTogo', requiresAuth: true },
  },

  // Espace admin/police (rôle requis)
  {
    path: '/admin',
    name: 'dashboard',
    component: () => import('../views/admin/DashboardView.vue'),
    meta: {
      title: 'Tableau de bord — DéclaTogo',
      requiresAuth: true,
      requiresStaff: true,
    },
  },
  {
    path: '/admin/declarations',
    name: 'admin-declarations',
    component: () => import('../views/admin/AdminDeclarationsView.vue'),
    meta: {
      title: 'Gestion des déclarations — DéclaTogo',
      requiresAuth: true,
      requiresStaff: true,
    },
  },

  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: { title: 'Page introuvable — DéclaTogo', public: true },
  },
]

// ── Création du router ─────────────────────────────────────────────
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  // Retour en haut de page à chaque navigation
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash)       return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

// ── Navigation Guard ───────────────────────────────────────────────
router.beforeEach(async (to, from, next) => {
  // Mise à jour du titre de la page
  document.title = to.meta.title || 'DéclaTogo'

  // Import du store (après que Pinia soit initialisé)
  const { useAuthStore } = await import('../stores/auth')
  const authStore = useAuthStore()

  // Initialisation au premier chargement
  if (!authStore.user && authStore.accessToken) {
    await authStore.init()
  }

  // Route réservée aux non-connectés (login, register)
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }

  // Route nécessitant une connexion
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Route nécessitant un rôle admin ou police
  if (to.meta.requiresStaff && !authStore.isStaff) {
    return next({ name: 'mes-declarations' })
  }

  next()
})

export default router