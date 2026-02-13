<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../../stores/auth'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const route = useRoute()

/* ── État du formulaire ── */
const form = ref({
  username: '',
  password: '',
  remember: false,
})
const showPassword  = ref(false)
const submitted     = ref(false)

/* ── Validation locale ── */
const errors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (!form.value.username.trim())      e.username = 'Nom d\'utilisateur requis'
  if (form.value.password.length < 3)   e.password = 'Mot de passe requis'
  return e
})
const isValid = computed(() => Object.keys(errors.value).length === 0)

/* ── Soumission ── */
async function handleLogin() {
  submitted.value = true
  if (!isValid.value) return

  await authStore.login({
    username: form.value.username.trim(),
    password: form.value.password,
  })
  // La redirection est gérée par le store
}

/* ── Bulles déco animées ── */
const bubbles = [
  { size: 120, top: '10%',  left: '15%', delay: '0s',   dur: '7s'  },
  { size: 60,  top: '65%',  left: '70%', delay: '1.2s', dur: '9s'  },
  { size: 90,  top: '40%',  left: '5%',  delay: '2.5s', dur: '11s' },
  { size: 45,  top: '80%',  left: '30%', delay: '0.7s', dur: '8s'  },
  { size: 75,  top: '20%',  left: '80%', delay: '3s',   dur: '10s' },
]
</script>

<template>
  <div class="min-h-screen flex overflow-hidden" style="background:#FAF7F2">

    <!-- ══════════════════════════════════════════
         PANNEAU GAUCHE — Identité de marque
    ══════════════════════════════════════════ -->
    <aside class="hidden lg:flex lg:w-[46%] flex-col relative overflow-hidden"
           style="background-color:#005A3C">

      <!-- Motif kente + gradient -->
      <div class="absolute inset-0 kente-bg opacity-40"></div>
      <div class="absolute inset-0 bg-gradient-to-br from-[#003d29] via-transparent to-[#001a0e]/70"></div>

      <!-- Bulles décoratives flottantes -->
      <div v-for="(b, i) in bubbles" :key="i"
        class="absolute rounded-full border border-white/10 bg-white/5"
        :style="{
          width: b.size + 'px', height: b.size + 'px',
          top: b.top, left: b.left,
          animation: `floatBubble ${b.dur} ${b.delay} ease-in-out infinite alternate`
        }">
      </div>

      <!-- Bande verticale drapeau togolais -->
      <div class="absolute left-0 inset-y-0 w-1.5 flex flex-col">
        <div class="flex-[2] bg-[#005A3C]"></div>
        <div class="flex-1 bg-[#FFCE00]"></div>
        <div class="flex-[2] bg-[#C41230]"></div>
      </div>

      <div class="relative z-10 flex flex-col h-full px-12 py-14">

        <!-- Logo -->
        <div class="flex items-center gap-3 mb-auto">
          <div class="w-11 h-11 bg-[#D4A017] rounded-xl flex items-center justify-center
                      font-serif font-bold text-[#005A3C] text-sm shadow-lg">DT</div>
          <span class="font-serif text-2xl font-bold text-white tracking-tight">
            Décla<span class="text-[#D4A017]">Togo</span>
          </span>
        </div>

        <!-- Contenu central -->
        <div class="my-auto">
          <!-- Décoratif : cercle étoile -->
          <div class="w-20 h-20 rounded-full border-2 border-[#D4A017]/40 flex items-center
                      justify-center mb-8 relative">
            <div class="w-12 h-12 bg-[#D4A017]/20 rounded-full flex items-center justify-center">
              <span class="text-2xl">🔐</span>
            </div>
            <div class="absolute inset-0 rounded-full border border-[#D4A017]/20 spin-slow"></div>
          </div>

          <h2 class="font-serif text-[2.8rem] font-bold text-white leading-[1.1] mb-5">
            Votre espace<br/>
            <span class="text-[#D4A017]">citoyen</span><br/>
            vous attend.
          </h2>
          <p class="text-white/70 text-sm leading-relaxed max-w-[320px]">
            Déclarez, suivez et retrouvez vos pièces administratives
            depuis n'importe où au Togo.
          </p>

          <!-- Trois avantages -->
          <div class="mt-9 space-y-3.5">
            <div v-for="item in [
              { icon:'🛡️', text:'Données chiffrées & sécurisées' },
              { icon:'📄', text:'Récépissé PDF officiel instantané' },
              { icon:'🔔', text:'Alertes en cas de correspondance' },
            ]" :key="item.text"
              class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm flex-shrink-0">
                {{ item.icon }}
              </span>
              <span class="text-sm text-white/80">{{ item.text }}</span>
            </div>
          </div>
        </div>

        <!-- Pied de panneau -->
        <p class="text-xs text-white/35 mt-auto">
          © 2025 DéclaTogo — République Togolaise
        </p>
      </div>
    </aside>


    <!-- ══════════════════════════════════════════
         PANNEAU DROIT — Formulaire de connexion
    ══════════════════════════════════════════ -->
    <main class="flex-1 flex flex-col items-center justify-center px-6 py-12 relative">

      <!-- Fond décoratif subtil -->
      <div class="absolute inset-0 pointer-events-none"
           style="background:radial-gradient(ellipse 60% 50% at 80% 20%, rgba(0,90,60,.04) 0%, transparent 70%)">
      </div>

      <!-- Logo mobile uniquement -->
      <div class="lg:hidden flex items-center gap-2 mb-8">
        <div class="w-9 h-9 bg-[#005A3C] rounded-lg flex items-center justify-center
                    font-serif font-bold text-[#D4A017] text-sm">DT</div>
        <span class="font-serif text-xl font-bold text-[#1A2E22]">
          Décla<span class="text-[#005A3C]">Togo</span>
        </span>
      </div>

      <div class="w-full max-w-[420px] fade-up relative z-10">

        <!-- En-tête -->
        <div class="mb-8">
          <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                      text-xs font-bold px-3 py-1.5 rounded-full mb-4">
            🇹🇬 Plateforme officielle
          </div>
          <h1 class="font-serif text-[2rem] font-bold text-[#1A2E22] leading-tight mb-1.5">
            {{ t('auth.login_title') }}
          </h1>
          <p class="text-sm text-gray-500">{{ t('auth.login_sub') }}</p>
        </div>

        <!-- Erreur API globale -->
        <transition name="slide-error">
          <div v-if="authStore.error"
            class="flex items-start gap-3 bg-red-50 border border-red-200
                   rounded-xl p-4 mb-6 text-sm text-rouge">
            <span class="text-lg leading-none mt-0.5">⚠️</span>
            <span>{{ authStore.error }}</span>
          </div>
        </transition>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" novalidate class="space-y-5">

          <!-- Nom d'utilisateur -->
          <div>
            <label class="form-label">{{ t('auth.username') }}</label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">👤</span>
              <input
                v-model="form.username"
                type="text"
                autocomplete="username"
                :placeholder="t('auth.username')"
                :class="['form-input pl-10', errors.username && 'border-rouge ring-2 ring-rouge/15']"
              />
            </div>
            <p v-if="errors.username" class="form-error">
              <span>✕</span> {{ errors.username }}
            </p>
          </div>

          <!-- Mot de passe -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="form-label mb-0">{{ t('auth.password') }}</label>
              <a href="#" class="text-xs text-[#005A3C] hover:underline">{{ t('auth.forgot') }}</a>
            </div>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                :placeholder="t('auth.password')"
                :class="['form-input pl-10 pr-12', errors.password && 'border-rouge ring-2 ring-rouge/15']"
              />
              <button type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                       hover:text-gray-600 transition-colors text-base bg-transparent border-none cursor-pointer">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
            <p v-if="errors.password" class="form-error">
              <span>✕</span> {{ errors.password }}
            </p>
          </div>

          <!-- Se souvenir de moi -->
          <div class="flex items-center gap-2.5">
            <button type="button"
              @click="form.remember = !form.remember"
              :class="[
                'w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0',
                'transition-all cursor-pointer border-none',
                form.remember ? 'bg-[#005A3C]' : 'bg-white border border-gray-300'
              ]"
              style="border: 2px solid; border-color: v-bind('form.remember ? \'#005A3C\' : \'#d1d5db\'')">
              <span v-if="form.remember" class="text-white text-xs leading-none">✓</span>
            </button>
            <span class="text-sm text-gray-500 cursor-pointer select-none"
              @click="form.remember = !form.remember">
              {{ t('auth.remember') }}
            </span>
          </div>

          <!-- Bouton connexion -->
          <button type="submit"
            :disabled="authStore.loading"
            class="w-full flex items-center justify-center gap-2.5
                   bg-[#005A3C] text-white font-bold py-3.5 px-6 rounded-[10px]
                   border-none cursor-pointer text-sm transition-all
                   hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg
                   disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0"
            :style="{ boxShadow: authStore.loading ? 'none' : '0 4px 16px rgba(0,90,60,.30)' }">
            <span v-if="authStore.loading" class="loader-dot"></span>
            <span v-else>🚀</span>
            <span>{{ authStore.loading ? 'Connexion en cours...' : t('auth.login_btn') }}</span>
          </button>

        </form>

        <!-- Séparateur -->
        <div class="flex items-center gap-3 my-6">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400 font-medium">ou</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>

        <!-- Lien inscription -->
        <p class="text-center text-sm text-gray-500">
          {{ t('auth.no_account') }}
          <router-link :to="{ name: 'register' }"
            class="text-[#005A3C] font-semibold hover:underline ml-1">
            {{ t('auth.register_link') }} →
          </router-link>
        </p>

        <!-- Retour accueil -->
        <div class="mt-6 text-center">
          <router-link :to="{ name: 'home' }"
            class="inline-flex items-center gap-1.5 text-xs text-gray-400
                   hover:text-[#005A3C] transition-colors no-underline">
            ← Retour à l'accueil
          </router-link>
        </div>

      </div>
    </main>

  </div>
</template>

<style scoped>
/* Animation bulle flottante */
@keyframes floatBubble {
  from { transform: translateY(0px) scale(1); opacity: .5; }
  to   { transform: translateY(-18px) scale(1.05); opacity: .8; }
}

/* Loader point animé */
.loader-dot {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Transition erreur */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to { opacity: 0; transform: translateY(-8px); max-height: 0; }

/* Override checkbox visuel */
button[style*="border-color"] {
  outline: none;
}
</style>