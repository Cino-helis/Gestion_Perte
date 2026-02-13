<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../../stores/auth'

const { t } = useI18n()
const authStore = useAuthStore()

/* ── Étape du formulaire wizard (2 étapes) ── */
const step = ref(1)
const submitted = ref(false)

/* ── État du formulaire ── */
const form = ref({
  first_name:       '',
  last_name:        '',
  username:         '',
  email:            '',
  telephone:        '',
  password:         '',
  password_confirm: '',
})
const showPassword        = ref(false)
const showPasswordConfirm = ref(false)

/* ── Validation par champ ── */
const fieldErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}

  // Étape 1
  if (!form.value.first_name.trim())  e.first_name = 'Prénom requis'
  if (!form.value.last_name.trim())   e.last_name  = 'Nom requis'
  if (!form.value.username.trim())    e.username   = 'Nom d\'utilisateur requis'
  if (form.value.username.trim().length < 3)
    e.username = 'Minimum 3 caractères'
  if (!/^[a-zA-Z0-9@.+\-_]+$/.test(form.value.username))
    e.username = 'Caractères autorisés : lettres, chiffres, @/./+/-/_'
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Adresse email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"

  // Étape 2
  if (form.value.password.length < 8)
    e.password = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(form.value.password))
    e.password = 'Doit contenir au moins une majuscule'
  if (!/[0-9]/.test(form.value.password))
    e.password = 'Doit contenir au moins un chiffre'
  if (form.value.password !== form.value.password_confirm)
    e.password_confirm = 'Les mots de passe ne correspondent pas'

  return e
})

/* ── Validation par étape ── */
const step1Valid = computed(() => {
  const e = fieldErrors.value
  return !e.first_name && !e.last_name && !e.username && !e.email && !e.telephone
})
const step2Valid = computed(() => {
  const e = fieldErrors.value
  return !e.password && !e.password_confirm
})

/* ── Forcer la validation à l'étape courante ── */
const validateStep1 = () => {
  submitted.value = true
  return step1Valid.value
}

const goToStep2 = () => {
  if (validateStep1()) step.value = 2
}

/* ── Indicateur de force du mot de passe ── */
const passwordStrength = computed(() => {
  const p = form.value.password
  if (!p) return { score: 0, label: '', color: '' }
  let score = 0
  if (p.length >= 8)  score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++

  const levels = [
    { score: 0, label: '',             color: 'bg-gray-200' },
    { score: 1, label: 'Très faible',  color: 'bg-red-400'  },
    { score: 2, label: 'Faible',       color: 'bg-orange-400' },
    { score: 3, label: 'Moyen',        color: 'bg-yellow-400' },
    { score: 4, label: 'Fort',         color: 'bg-green-400' },
    { score: 5, label: 'Très fort',    color: 'bg-[#005A3C]' },
  ]
  return levels[score] || levels[4]
})

/* ── Soumission finale ── */
async function handleRegister() {
  submitted.value = true
  if (!step2Valid.value || !step1Valid.value) return

  await authStore.register({
    first_name:       form.value.first_name.trim(),
    last_name:        form.value.last_name.trim(),
    username:         form.value.username.trim(),
    email:            form.value.email.trim(),
    telephone:        form.value.telephone.trim(),
    password:         form.value.password,
    password_confirm: form.value.password_confirm,
  })
}

/* ── Labels des étapes ── */
const steps = [
  { num: 1, label: 'Informations personnelles', icon: '👤' },
  { num: 2, label: 'Sécurité',                  icon: '🔐' },
]
</script>

<template>
  <div class="min-h-screen flex overflow-hidden" style="background:#FAF7F2">

    <!-- ══════════════════════════════════════════
         PANNEAU GAUCHE — Identité de marque
    ══════════════════════════════════════════ -->
    <aside class="hidden lg:flex lg:w-[46%] flex-col relative overflow-hidden"
           style="background-color:#C41230">

      <div class="absolute inset-0 kente-bg opacity-30"></div>
      <div class="absolute inset-0 bg-gradient-to-bl from-[#8B0D22] via-transparent to-[#3d0010]/60"></div>

      <!-- Bande drapeau -->
      <div class="absolute left-0 inset-y-0 w-1.5 flex flex-col">
        <div class="flex-[2] bg-[#005A3C]"></div>
        <div class="flex-1 bg-[#FFCE00]"></div>
        <div class="flex-[2] bg-[#C41230]"></div>
      </div>

      <!-- Cercles décoratifs -->
      <div class="absolute top-[-60px] right-[-60px] w-64 h-64 rounded-full
                  border border-white/10 opacity-50"></div>
      <div class="absolute bottom-[-40px] left-[-40px] w-48 h-48 rounded-full
                  border border-white/10 opacity-50"></div>

      <div class="relative z-10 flex flex-col h-full px-12 py-14">

        <!-- Logo -->
        <div class="flex items-center gap-3 mb-auto">
          <div class="w-11 h-11 bg-[#D4A017] rounded-xl flex items-center justify-center
                      font-serif font-bold text-[#005A3C] text-sm shadow-lg">DT</div>
          <span class="font-serif text-2xl font-bold text-white tracking-tight">
            Décla<span class="text-[#D4A017]">Togo</span>
          </span>
        </div>

        <div class="my-auto">
          <div class="w-20 h-20 rounded-full border-2 border-[#D4A017]/40 flex items-center
                      justify-center mb-8 relative">
            <div class="w-12 h-12 bg-[#D4A017]/20 rounded-full flex items-center justify-center">
              <span class="text-2xl">🎉</span>
            </div>
          </div>

          <h2 class="font-serif text-[2.8rem] font-bold text-white leading-[1.1] mb-5">
            Rejoignez<br/>
            <span class="text-[#D4A017]">des milliers</span><br/>
            de citoyens.
          </h2>
          <p class="text-white/70 text-sm leading-relaxed max-w-[320px]">
            Inscription gratuite, récépissé immédiat. Votre espace sécurisé
            pour gérer vos déclarations administratives.
          </p>

          <!-- Chiffres clés -->
          <div class="mt-10 grid grid-cols-2 gap-4">
            <div v-for="stat in [
              { num:'2 847+', label:'Déclarations' },
              { num:'1 203+', label:'Pièces retrouvées' },
              { num:'847+',   label:'Citoyens inscrits' },
              { num:'42%',    label:'Taux de restitution' },
            ]" :key="stat.label"
              class="bg-white/10 rounded-xl p-4 border border-white/10">
              <div class="font-serif text-2xl font-bold text-[#D4A017] leading-none mb-1">
                {{ stat.num }}
              </div>
              <div class="text-xs text-white/60">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <p class="text-xs text-white/35 mt-auto">
          © 2025 DéclaTogo — République Togolaise
        </p>
      </div>
    </aside>


    <!-- ══════════════════════════════════════════
         PANNEAU DROIT — Formulaire d'inscription
    ══════════════════════════════════════════ -->
    <main class="flex-1 flex flex-col items-center justify-center px-6 py-10 relative">

      <div class="absolute inset-0 pointer-events-none"
           style="background:radial-gradient(ellipse 60% 50% at 20% 80%, rgba(196,18,48,.04) 0%, transparent 70%)">
      </div>

      <!-- Logo mobile -->
      <div class="lg:hidden flex items-center gap-2 mb-8">
        <div class="w-9 h-9 bg-[#C41230] rounded-lg flex items-center justify-center
                    font-serif font-bold text-white text-sm">DT</div>
        <span class="font-serif text-xl font-bold text-[#1A2E22]">
          Décla<span class="text-[#C41230]">Togo</span>
        </span>
      </div>

      <div class="w-full max-w-[460px] fade-up relative z-10">

        <!-- En-tête -->
        <div class="mb-6">
          <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                      text-xs font-bold px-3 py-1.5 rounded-full mb-4">
            🆕 Inscription gratuite
          </div>
          <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] leading-tight mb-1">
            {{ t('auth.register_title') }}
          </h1>
          <p class="text-sm text-gray-500">{{ t('auth.register_sub') }}</p>
        </div>

        <!-- Stepper -->
        <div class="flex items-center gap-0 mb-7">
          <div v-for="(s, i) in steps" :key="s.num" class="flex items-center flex-1">
            <div class="flex items-center gap-2">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all',
                step === s.num
                  ? 'bg-[#005A3C] text-white shadow-md'
                  : step > s.num
                    ? 'bg-[#005A3C]/20 text-[#005A3C]'
                    : 'bg-gray-200 text-gray-400'
              ]">
                <span v-if="step > s.num">✓</span>
                <span v-else>{{ s.num }}</span>
              </div>
              <span :class="[
                'text-xs font-medium hidden sm:block transition-colors',
                step === s.num ? 'text-[#1A2E22]' : 'text-gray-400'
              ]">{{ s.label }}</span>
            </div>
            <div v-if="i < steps.length - 1"
              :class="[
                'flex-1 h-px mx-3 transition-all',
                step > s.num ? 'bg-[#005A3C]' : 'bg-gray-200'
              ]">
            </div>
          </div>
        </div>

        <!-- Erreur API globale -->
        <transition name="slide-error">
          <div v-if="authStore.error"
            class="flex items-start gap-3 bg-red-50 border border-red-200
                   rounded-xl p-4 mb-5 text-sm text-rouge">
            <span class="text-lg leading-none mt-0.5">⚠️</span>
            <span>{{ authStore.error }}</span>
          </div>
        </transition>

        <!-- ═══════════════ ÉTAPE 1 ═══════════════ -->
        <transition name="step-slide" mode="out-in">
          <div v-if="step === 1" key="step1" class="space-y-4">

            <!-- Prénom + Nom (côte à côte) -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="form-label">{{ t('auth.first_name') }}</label>
                <input
                  v-model="form.first_name"
                  type="text"
                  autocomplete="given-name"
                  :placeholder="t('auth.first_name')"
                  :class="['form-input', fieldErrors.first_name && 'border-rouge ring-2 ring-rouge/15']"
                />
                <p v-if="fieldErrors.first_name" class="form-error">
                  <span>✕</span> {{ fieldErrors.first_name }}
                </p>
              </div>
              <div>
                <label class="form-label">{{ t('auth.last_name') }}</label>
                <input
                  v-model="form.last_name"
                  type="text"
                  autocomplete="family-name"
                  :placeholder="t('auth.last_name')"
                  :class="['form-input', fieldErrors.last_name && 'border-rouge ring-2 ring-rouge/15']"
                />
                <p v-if="fieldErrors.last_name" class="form-error">
                  <span>✕</span> {{ fieldErrors.last_name }}
                </p>
              </div>
            </div>

            <!-- Nom d'utilisateur -->
            <div>
              <label class="form-label">{{ t('auth.username') }}</label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">@</span>
                <input
                  v-model="form.username"
                  type="text"
                  autocomplete="username"
                  placeholder="jean_akodjo"
                  :class="['form-input pl-8', fieldErrors.username && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.username" class="form-error">
                <span>✕</span> {{ fieldErrors.username }}
              </p>
            </div>

            <!-- Email -->
            <div>
              <label class="form-label">{{ t('auth.email') }} <span class="text-gray-400 normal-case font-normal">(optionnel)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✉️</span>
                <input
                  v-model="form.email"
                  type="email"
                  autocomplete="email"
                  :placeholder="t('auth.email')"
                  :class="['form-input pl-10', fieldErrors.email && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.email" class="form-error">
                <span>✕</span> {{ fieldErrors.email }}
              </p>
            </div>

            <!-- Téléphone -->
            <div>
              <label class="form-label">{{ t('auth.phone') }} <span class="text-gray-400 normal-case font-normal">(optionnel)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm text-nowrap">🇹🇬</span>
                <input
                  v-model="form.telephone"
                  type="tel"
                  autocomplete="tel"
                  placeholder="+22890123456"
                  :class="['form-input pl-10', fieldErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.telephone" class="form-error">
                <span>✕</span> {{ fieldErrors.telephone }}
              </p>
            </div>

            <!-- Bouton suivant -->
            <button type="button"
              @click="goToStep2"
              class="w-full flex items-center justify-center gap-2.5
                     bg-[#005A3C] text-white font-bold py-3.5 px-6 rounded-[10px]
                     border-none cursor-pointer text-sm transition-all mt-2
                     hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg"
              style="box-shadow: 0 4px 16px rgba(0,90,60,.30)">
              Continuer →
            </button>
          </div>
        </transition>

        <!-- ═══════════════ ÉTAPE 2 ═══════════════ -->
        <transition name="step-slide" mode="out-in">
          <div v-if="step === 2" key="step2">

            <form @submit.prevent="handleRegister" novalidate class="space-y-4">

              <!-- Résumé étape 1 -->
              <div class="flex items-center gap-3 bg-[#E8F4F0] rounded-xl p-3.5 mb-2">
                <div class="w-9 h-9 bg-[#005A3C] rounded-full flex items-center justify-center
                            text-white text-base font-serif font-bold flex-shrink-0">
                  {{ form.first_name.charAt(0).toUpperCase() || '?' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-semibold text-[#1A2E22] truncate">
                    {{ form.first_name }} {{ form.last_name }}
                  </div>
                  <div class="text-xs text-gray-500 truncate">@{{ form.username }}</div>
                </div>
                <button type="button"
                  @click="step = 1"
                  class="text-xs text-[#005A3C] font-semibold bg-transparent border-none
                         cursor-pointer hover:underline flex-shrink-0">
                  Modifier
                </button>
              </div>

              <!-- Mot de passe -->
              <div>
                <label class="form-label">{{ t('auth.password') }}</label>
                <div class="relative">
                  <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="new-password"
                    :placeholder="t('auth.password')"
                    :class="['form-input pl-10 pr-12', fieldErrors.password && 'border-rouge ring-2 ring-rouge/15']"
                  />
                  <button type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                           hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
                    {{ showPassword ? '🙈' : '👁️' }}
                  </button>
                </div>

                <!-- Barre de force -->
                <div v-if="form.password" class="mt-2">
                  <div class="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                    <div :class="['h-full rounded-full transition-all duration-500', passwordStrength.color]"
                      :style="{ width: `${(passwordStrength.score / 5) * 100}%` }">
                    </div>
                  </div>
                  <p class="text-xs mt-1" :class="{
                    'text-red-400': passwordStrength.score <= 2,
                    'text-yellow-600': passwordStrength.score === 3,
                    'text-[#005A3C]': passwordStrength.score >= 4,
                  }">{{ passwordStrength.label }}</p>
                </div>
                <p v-if="fieldErrors.password" class="form-error">
                  <span>✕</span> {{ fieldErrors.password }}
                </p>
              </div>

              <!-- Confirmer mot de passe -->
              <div>
                <label class="form-label">{{ t('auth.pwd_confirm') }}</label>
                <div class="relative">
                  <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔑</span>
                  <input
                    v-model="form.password_confirm"
                    :type="showPasswordConfirm ? 'text' : 'password'"
                    autocomplete="new-password"
                    :placeholder="t('auth.pwd_confirm')"
                    :class="['form-input pl-10 pr-12', fieldErrors.password_confirm && 'border-rouge ring-2 ring-rouge/15']"
                  />
                  <button type="button"
                    @click="showPasswordConfirm = !showPasswordConfirm"
                    class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                           hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
                    {{ showPasswordConfirm ? '🙈' : '👁️' }}
                  </button>
                </div>

                <!-- Check visuel : les mots de passe correspondent -->
                <div v-if="form.password_confirm && form.password === form.password_confirm"
                  class="flex items-center gap-1.5 mt-1.5">
                  <span class="text-green-500 text-xs">✓ Les mots de passe correspondent</span>
                </div>
                <p v-if="fieldErrors.password_confirm" class="form-error">
                  <span>✕</span> {{ fieldErrors.password_confirm }}
                </p>
              </div>

              <!-- Critères de sécurité -->
              <ul class="text-xs text-gray-400 space-y-1 list-none pl-0 bg-gray-50 rounded-xl p-3">
                <li v-for="rule in [
                  { ok: form.password.length >= 8,          text: 'Minimum 8 caractères' },
                  { ok: /[A-Z]/.test(form.password),        text: 'Au moins une majuscule' },
                  { ok: /[0-9]/.test(form.password),        text: 'Au moins un chiffre' },
                  { ok: /[^A-Za-z0-9]/.test(form.password), text: 'Caractère spécial recommandé' },
                ]" :key="rule.text"
                  :class="['flex items-center gap-2', rule.ok ? 'text-[#005A3C]' : 'text-gray-400']">
                  <span>{{ rule.ok ? '✓' : '○' }}</span> {{ rule.text }}
                </li>
              </ul>

              <!-- Boutons -->
              <div class="flex gap-3 mt-2">
                <button type="button"
                  @click="step = 1"
                  class="flex-shrink-0 px-5 py-3.5 rounded-[10px] border border-gray-200
                         text-sm font-medium text-gray-500 bg-white hover:bg-gray-50
                         transition-all cursor-pointer">
                  ← Retour
                </button>

                <button type="submit"
                  :disabled="authStore.loading"
                  class="flex-1 flex items-center justify-center gap-2.5
                         bg-[#C41230] text-white font-bold py-3.5 px-6 rounded-[10px]
                         border-none cursor-pointer text-sm transition-all
                         hover:bg-[#e8192f] hover:-translate-y-0.5 hover:shadow-lg
                         disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0">
                  <span v-if="authStore.loading" class="loader-dot"></span>
                  <span v-else>🎉</span>
                  <span>{{ authStore.loading ? 'Création...' : t('auth.register_btn') }}</span>
                </button>
              </div>

            </form>
          </div>
        </transition>

        <!-- Séparateur + lien connexion -->
        <div class="flex items-center gap-3 mt-6 mb-4">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400 font-medium">ou</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>

        <p class="text-center text-sm text-gray-500">
          {{ t('auth.have_account') }}
          <router-link :to="{ name: 'login' }"
            class="text-[#005A3C] font-semibold hover:underline ml-1">
            {{ t('auth.login_link') }} →
          </router-link>
        </p>

        <div class="mt-4 text-center">
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
/* Transition entre étapes */
.step-slide-enter-active,
.step-slide-leave-active { transition: all .3s ease; }
.step-slide-enter-from   { opacity: 0; transform: translateX(30px); }
.step-slide-leave-to     { opacity: 0; transform: translateX(-30px); }

/* Erreur API */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to     { opacity: 0; transform: translateY(-8px); }

/* Spinner */
.loader-dot {
  display: inline-block;
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>