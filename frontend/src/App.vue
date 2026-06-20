<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from './stores/auth'
import { notificationsAPI, adminRemplacementsAPI } from './services/api'

const route        = useRoute()
const { t, locale } = useI18n()
const authStore    = useAuthStore()
const mobileOpen   = ref(false)
const unreadCount  = ref(0)
const remplacementsBadge = ref(0)   // ← badge dossiers en attente

const toggleLang = () => {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
}

const handleLogout = () => {
  authStore.logout()
  mobileOpen.value      = false
  unreadCount.value     = 0
  remplacementsBadge.value = 0
}

// ── Notifications non lues ─────────────────────────────────────────────────
const fetchUnread = async () => {
  if (!authStore.isAuthenticated) return
  try {
    const { data } = await notificationsAPI.nonLues()
    unreadCount.value = (data.results ?? data).length
  } catch { unreadCount.value = 0 }
}

// ── Badge remplacements en attente (staff seulement) ──────────────────────
const fetchRemplacementsBadge = async () => {
  if (!authStore.isStaff) return
  try {
    const { data } = await adminRemplacementsAPI.list({ statut: 'EN_ATTENTE' })
    remplacementsBadge.value = (data.results ?? data).length
  } catch { remplacementsBadge.value = 0 }
}

// Rafraîchit les badges à chaque changement de page
watch(route, () => {
  mobileOpen.value = false
  fetchUnread()
  fetchRemplacementsBadge()
})

// Charge les badges dès que l'utilisateur est connecté
watch(() => authStore.isAuthenticated, (auth) => {
  if (auth) {
    fetchUnread()
    fetchRemplacementsBadge()
  } else {
    unreadCount.value        = 0
    remplacementsBadge.value = 0
  }
}, { immediate: true })
</script>

<template>
  <!-- ── Bandeau d'annonce ── -->
  <div class="bg-or text-vert text-xs font-semibold text-center py-2.5 px-4 flex items-center justify-center gap-2">
    ✨ {{ t('announce') }}
  </div>

  <!-- ══════════════════════════════════════════
       NAVIGATION DESKTOP
  ══════════════════════════════════════════ -->
  <nav class="sticky top-0 z-50 flex items-center justify-between px-[5%] h-[68px]
              bg-vert/95 backdrop-blur border-b-2 border-or">

    <!-- Logo -->
    <router-link :to="{ name: 'home' }"
      class="flex items-center gap-3 text-white font-serif text-xl font-bold no-underline">
      <div class="w-9 h-9 bg-or rounded-lg flex items-center justify-center text-vert font-bold text-sm">
        TG
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" class="w-7 h-5 rounded-sm shadow-sm flex-shrink-0">
        <rect width="900" height="600" fill="#006A4E"/>
        <rect width="900" height="120" y="0"   fill="#006A4E"/>
        <rect width="900" height="120" y="120" fill="#FFCE00"/>
        <rect width="900" height="120" y="240" fill="#006A4E"/>
        <rect width="900" height="120" y="360" fill="#FFCE00"/>
        <rect width="900" height="120" y="480" fill="#006A4E"/>
        <rect width="300" height="600" fill="#D21034"/>
        <polygon points="150,100 179,191 271,191 198,246 224,337 150,282 76,337 102,246 29,191 121,191"
                 fill="#FFCE00"/>
      </svg>
      Décla<span class="text-or">Togo</span>
    </router-link>

    <!-- Liens desktop -->
    <div class="hidden md:flex items-center gap-1">

      <!-- Liens publics -->
      <router-link :to="{ name: 'home' }"   class="nav-desktop-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-desktop-link">{{ t('nav.search') }}</router-link>

      <!-- Liens connectés -->
      <template v-if="authStore.isAuthenticated">

        <router-link :to="{ name: 'declare' }" class="nav-desktop-link">
          {{ t('nav.declare') }}
        </router-link>

        <!-- Mes déclarations -->
        <router-link :to="{ name: 'mes-declarations' }" class="nav-desktop-link">
          📋 Mes déclarations
        </router-link>

        <!-- Notifications -->
        <router-link :to="{ name: 'notifications' }" class="nav-desktop-link relative">
          🔔 Notifications
          <span v-if="unreadCount > 0"
            class="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-rouge text-white
                   text-[10px] font-bold rounded-full flex items-center justify-center
                   px-1 leading-none shadow">
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </span>
        </router-link>

        <!-- Tableau de bord admin/police -->
        <router-link v-if="authStore.isStaff" :to="{ name: 'dashboard' }" class="nav-desktop-link">
          {{ t('nav.dashboard') }}
        </router-link>

        <!-- ── Remplacements (staff) ── -->
        <router-link v-if="authStore.isStaff"
          :to="{ name: 'admin-remplacements' }"
          class="nav-desktop-link relative">
          🔄 Remplacements
          <span v-if="remplacementsBadge > 0"
            class="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-[#7C3AED] text-white
                   text-[10px] font-bold rounded-full flex items-center justify-center
                   px-1 leading-none shadow">
            {{ remplacementsBadge > 99 ? '99+' : remplacementsBadge }}
          </span>
        </router-link>

      </template>

      <!-- Sélecteur langue -->
      <button @click="toggleLang" class="lang-btn">
        🌐 {{ locale.toUpperCase() }}
      </button>

      <!-- Non connecté -->
      <template v-if="!authStore.isAuthenticated">
        <router-link :to="{ name: 'login' }"    class="nav-desktop-link">{{ t('nav.login') }}</router-link>
        <router-link :to="{ name: 'register' }" class="register-btn">{{ t('nav.register') }}</router-link>
      </template>

      <!-- Connecté — bouton déconnexion -->
      <button v-else @click="handleLogout" class="logout-btn">
        {{ t('nav.logout') }}
      </button>

    </div>

    <!-- Bouton hamburger mobile -->
    <button @click="mobileOpen = !mobileOpen"
      class="md:hidden text-white text-2xl bg-transparent border-none">
      {{ mobileOpen ? '✕' : '☰' }}
    </button>
  </nav>

  <!-- ══════════════════════════════════════════
       MENU MOBILE
  ══════════════════════════════════════════ -->
  <transition name="slide-down">
    <div v-if="mobileOpen"
      class="md:hidden fixed top-[108px] inset-x-0 z-40 bg-vert/98 backdrop-blur
             border-b border-or/30 flex flex-col gap-1 px-4 py-4">

      <!-- Logo mobile dans le menu -->
      <div class="flex items-center gap-2 px-4 pb-3 mb-1 border-b border-white/10">
        <div class="w-8 h-8 bg-or rounded-lg flex items-center justify-center text-vert font-bold text-xs">TG</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" class="w-7 h-5 rounded-sm shadow-sm flex-shrink-0">
          <rect width="900" height="600" fill="#006A4E"/>
          <rect width="900" height="120" y="0"   fill="#006A4E"/>
          <rect width="900" height="120" y="120" fill="#FFCE00"/>
          <rect width="900" height="120" y="240" fill="#006A4E"/>
          <rect width="900" height="120" y="360" fill="#FFCE00"/>
          <rect width="900" height="120" y="480" fill="#006A4E"/>
          <rect width="300" height="600" fill="#D21034"/>
          <polygon points="150,100 179,191 271,191 198,246 224,337 150,282 76,337 102,246 29,191 121,191"
                   fill="#FFCE00"/>
        </svg>
        <span class="font-serif text-lg font-bold text-white">Décla<span class="text-or">Togo</span></span>
      </div>

      <router-link :to="{ name: 'home' }"   class="nav-mobile-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-mobile-link">{{ t('nav.search') }}</router-link>

      <template v-if="authStore.isAuthenticated">

        <router-link :to="{ name: 'declare' }" class="nav-mobile-link">
          {{ t('nav.declare') }}
        </router-link>

        <!-- Mes déclarations (mobile) -->
        <router-link :to="{ name: 'mes-declarations' }" class="nav-mobile-link">
          📋 Mes déclarations
        </router-link>

        <!-- Notifications (mobile) -->
        <router-link :to="{ name: 'notifications' }"
          class="nav-mobile-link flex items-center justify-between">
          <span>🔔 Notifications</span>
          <span v-if="unreadCount > 0"
            class="min-w-[20px] h-5 bg-rouge text-white text-[10px] font-bold
                   rounded-full flex items-center justify-center px-1.5 leading-none">
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </span>
        </router-link>

        <!-- Dashboard (mobile) -->
        <router-link v-if="authStore.isStaff" :to="{ name: 'dashboard' }" class="nav-mobile-link">
          {{ t('nav.dashboard') }}
        </router-link>

        <!-- ── Remplacements (mobile, staff) ── -->
        <router-link v-if="authStore.isStaff"
          :to="{ name: 'admin-remplacements' }"
          class="nav-mobile-link flex items-center justify-between">
          <span>🔄 Remplacements</span>
          <span v-if="remplacementsBadge > 0"
            class="min-w-[20px] h-5 bg-[#7C3AED] text-white text-[10px] font-bold
                   rounded-full flex items-center justify-center px-1.5 leading-none">
            {{ remplacementsBadge > 99 ? '99+' : remplacementsBadge }}
          </span>
        </router-link>

        <div class="my-1 border-t border-white/10"></div>

        <button @click="handleLogout"
          class="nav-mobile-link text-left"
          style="color: #ff6b6b;">
          🚪 {{ t('nav.logout') }}
        </button>

      </template>

      <template v-else>
        <router-link :to="{ name: 'login' }"    class="nav-mobile-link">{{ t('nav.login') }}</router-link>
        <router-link :to="{ name: 'register' }" class="nav-mobile-link">{{ t('nav.register') }}</router-link>
      </template>

    </div>
  </transition>

  <!-- ══ Contenu des pages ══ -->
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" :key="route.fullPath" />
    </transition>
  </router-view>
</template>

<style scoped>
/* ── Navigation desktop ── */
.nav-desktop-link {
  @apply relative text-white/80 hover:text-white hover:bg-white/10
         px-3 py-2 rounded-lg text-sm font-medium transition-all no-underline;
}
.router-link-active.nav-desktop-link {
  @apply text-white bg-white/15;
}

/* ── Boutons spéciaux ── */
.register-btn {
  @apply bg-or text-vert font-bold text-sm px-5 py-2.5 rounded-lg no-underline
         hover:bg-[#e8b220] transition-all;
}
.logout-btn {
  @apply bg-rouge text-white font-semibold text-sm px-4 py-2 rounded-lg
         border-none cursor-pointer transition-all hover:bg-[#e8192f];
}
.lang-btn {
  @apply text-xs border border-white/30 px-2.5 py-1.5 rounded-lg
         text-white/70 bg-transparent cursor-pointer hover:border-white/60
         hover:text-white transition-all;
}

/* ── Navigation mobile ── */
.nav-mobile-link {
  @apply block text-sm font-medium px-4 py-3 rounded-lg transition-all no-underline;
  color: rgba(255, 255, 255, 0.85);
}
.nav-mobile-link:hover {
  background-color: rgba(255, 255, 255, 0.10);
  color: #ffffff;
}
.router-link-active.nav-mobile-link {
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}

/* ── Transitions ── */
.fade-enter-active,
.fade-leave-active       { transition: opacity .2s ease; }
.fade-enter-from,
.fade-leave-to           { opacity: 0; }

.slide-down-enter-active,
.slide-down-leave-active { transition: all .25s ease; }
.slide-down-enter-from,
.slide-down-leave-to     { opacity: 0; transform: translateY(-10px); }
</style>