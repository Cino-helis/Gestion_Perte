<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from './stores/auth'

const route = useRoute()
const { t, locale } = useI18n()
const authStore = useAuthStore()
const mobileOpen = ref(false)

const toggleLang = () => {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
}

const handleLogout = () => {
  authStore.logout()
  mobileOpen.value = false
}

watch(route, () => { mobileOpen.value = false })
</script>

<template>
  <div class="bg-or text-vert text-xs font-semibold text-center py-2.5 px-4 flex items-center justify-center gap-2">
    ✨ {{ t('announce') }}
  </div>

  <nav class="sticky top-0 z-50 flex items-center justify-between px-[5%] h-[68px] bg-vert/95 backdrop-blur border-b-2 border-or">
    <router-link :to="{ name: 'home' }" class="flex items-center gap-3 text-white font-serif text-xl font-bold no-underline">
      <div class="w-9 h-9 bg-or rounded-lg flex items-center justify-center text-vert font-bold text-sm">DT</div>
      Décla<span class="text-or">Togo</span>
    </router-link>

    <div class="hidden md:flex items-center gap-2">
      <router-link :to="{ name: 'home' }" class="nav-desktop-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-desktop-link">{{ t('nav.search') }}</router-link>

      <template v-if="authStore.isAuthenticated">
        <router-link :to="{ name: 'declare' }" class="nav-desktop-link">{{ t('nav.declare') }}</router-link>
        <router-link v-if="authStore.isStaff" :to="{ name: 'dashboard' }" class="nav-desktop-link">{{ t('nav.dashboard') }}</router-link>
      </template>

      <button @click="toggleLang" class="lang-btn">🌐 {{ locale.toUpperCase() }}</button>

      <template v-if="!authStore.isAuthenticated">
        <router-link :to="{ name: 'login' }" class="nav-desktop-link">{{ t('nav.login') }}</router-link>
        <router-link :to="{ name: 'register' }" class="register-btn">{{ t('nav.register') }}</router-link>
      </template>
      <button v-else @click="handleLogout" class="logout-btn">{{ t('nav.logout') }}</button>
    </div>

    <button @click="mobileOpen = !mobileOpen" class="md:hidden text-white text-2xl bg-transparent border-none">
      {{ mobileOpen ? '✕' : '☰' }}
    </button>
  </nav>

  <transition name="slide-down">
    <div v-if="mobileOpen" class="md:hidden fixed top-[108px] inset-x-0 z-40 bg-vert/98 backdrop-blur border-b border-or/30 flex flex-col gap-1 px-4 py-4">
      <router-link :to="{ name: 'home' }" class="nav-mobile-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-mobile-link">{{ t('nav.search') }}</router-link>
      <button v-if="authStore.isAuthenticated" @click="handleLogout" class="nav-mobile-link text-left text-rouge">
        {{ t('nav.logout') }}
      </button>
    </div>
  </transition>

  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style scoped>
.nav-desktop-link {
  @apply text-white/80 hover:text-white hover:bg-white/10 px-3 py-2 rounded-lg text-sm font-medium transition-all no-underline;
}
.register-btn {
  @apply bg-or text-vert font-bold text-sm px-5 py-2.5 rounded-lg no-underline hover:bg-[#e8b220] transition-all;
}
.logout-btn {
  @apply bg-rouge text-white font-semibold text-sm px-4 py-2 rounded-lg border-none cursor-pointer;
}
.lang-btn {
  @apply text-xs border border-white/30 px-2.5 py-1.5 rounded-lg text-white/70 bg-transparent cursor-pointer;
}

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-down-enter-active, .slide-down-leave-active { transition: all .25s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }
</style>