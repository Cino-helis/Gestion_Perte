/**
 * Vue Router — DéclaTogo
 */

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // ── Pages publiques ─────────────────────────────────────────────
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

  // ── Authentification ─────────────────────────────────────────────
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

  // ── Espace citoyen ───────────────────────────────────────────────
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

  // ── Espace admin / police ────────────────────────────────────────
  {
    path: '/admin',
    name: 'dashboard',
    component: () => import('../views/admin/DashboardView.vue'),
    meta: { title: 'Tableau de bord — DéclaTogo', requiresAuth: true, requiresStaff: true },
  },
  {
    path: '/admin/declarations',
    name: 'admin-declarations',
    component: () => import('../views/admin/AdminDeclarationsView.vue'),
    meta: {
      title: 'Gestion déclarations — DéclaTogo',
      requiresAuth: true,
      requiresStaff: true,
    },
  },
  {
    path: '/admin/agents',
    name: 'admin-agents',
    component: () => import('../views/admin/ManageAgentsView.vue'),
    meta: {
      title: 'Gestion des agents — DéclaTogo',
      requiresAuth: true,
      requiresAdmin: true,
    },
  },

  // ── Gestion utilisateurs — ADMIN UNIQUEMENT ──────────────────────
  {
    path: '/admin/utilisateurs',
    name: 'admin-users',
    component: () => import('../views/admin/ManageUsersView.vue'),
    meta: {
      title: 'Gestion des utilisateurs — DéclaTogo',
      requiresAuth: true,
      requiresAdmin: true,
    },
  },

  // ── 404 ──────────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: { title: 'Page introuvable — DéclaTogo', public: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash)       return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'DéclaTogo'

  const { useAuthStore } = await import('../stores/auth')
  const authStore = useAuthStore()

  if (!authStore.user && authStore.accessToken) {
    await authStore.init()
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Route réservée aux admins uniquement
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: 'dashboard' })
  }

  // Route réservée au staff (admin + police)
  if (to.meta.requiresStaff && !authStore.isStaff) {
    return next({ name: 'mes-declarations' })
  }

  next()
})

export default router