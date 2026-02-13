<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

/* ══ État ══ */
const tab          = ref('info')   // 'info' | 'password'
const submitting   = ref(false)
const success      = ref(null)
const apiError     = ref(null)
const submitted    = ref(false)

/* ══ Formulaire infos ══ */
const form = ref({
  first_name: '',
  last_name:  '',
  email:      '',
  telephone:  '',
})

/* ══ Formulaire mot de passe ══ */
const pwdForm = ref({
  current_password: '',
  new_password:     '',
  confirm_password: '',
})
const showPwd = ref({ current: false, new: false, confirm: false })

/* ══ Pré-remplir depuis le store ══ */
onMounted(() => {
  const u = authStore.user
  if (!u) return
  form.value = {
    first_name: u.first_name || '',
    last_name:  u.last_name  || '',
    email:      u.email      || '',
    telephone:  u.telephone  || '',
  }
})

/* ══ Validation ══ */
const infoErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Adresse email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"
  return e
})

const pwdErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (!pwdForm.value.current_password)       e.current = 'Requis'
  if (pwdForm.value.new_password.length < 8) e.new = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(pwdForm.value.new_password)) e.new = 'Au moins une majuscule'
  if (!/[0-9]/.test(pwdForm.value.new_password)) e.new = 'Au moins un chiffre'
  if (pwdForm.value.new_password !== pwdForm.value.confirm_password)
    e.confirm = 'Les mots de passe ne correspondent pas'
  return e
})

/* ══ Sauvegarde infos ══ */
const saveInfo = async () => {
  submitted.value = true
  if (Object.keys(infoErrors.value).length) return
  submitting.value = true
  success.value    = null
  apiError.value   = null
  const result = await authStore.updateProfile(form.value)
  if (result.success) {
    success.value = 'Profil mis à jour avec succès !'
  } else {
    apiError.value = result.error
  }
  submitting.value = false
  submitted.value  = false
}

/* ══ Changer mot de passe (via updateProfile) ══ */
const savePassword = async () => {
  submitted.value = true
  if (Object.keys(pwdErrors.value).length) return
  submitting.value = true
  success.value    = null
  apiError.value   = null
  // DRF attendrait un endpoint dédié; on envoie via PUT profil
  // En prod il faudrait un endpoint /api/change-password/ custom
  const result = await authStore.updateProfile({
    password:         pwdForm.value.new_password,
    current_password: pwdForm.value.current_password,
  })
  if (result.success) {
    success.value = 'Mot de passe modifié avec succès !'
    pwdForm.value = { current_password: '', new_password: '', confirm_password: '' }
  } else {
    apiError.value = result.error
  }
  submitting.value = false
  submitted.value  = false
}

/* ══ Initiale avatar ══ */
const initials = computed(() => {
  const u = authStore.user
  if (!u) return '?'
  if (u.first_name && u.last_name)
    return (u.first_name[0] + u.last_name[0]).toUpperCase()
  return u.username?.[0]?.toUpperCase() || '?'
})

const roleLabel = {
  citoyen: { text: 'Citoyen',          bg: '#E8F4F0', color: '#005A3C' },
  police:  { text: 'Agent de Police',  bg: '#DBEAFE', color: '#2563EB' },
  admin:   { text: 'Administrateur',   bg: '#FEE2E2', color: '#C41230' },
}
const role = computed(() => roleLabel[authStore.user?.role] || roleLabel.citoyen)

const clearMessages = () => { success.value = null; apiError.value = null; submitted.value = false }
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-2xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="mb-8">
    <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                text-xs font-bold px-3 py-1.5 rounded-full mb-3">
      👤 Mon profil
    </div>
    <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22]">
      Gérer mon compte
    </h1>
  </div>

  <!-- ══ Carte avatar ══ -->
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 mb-5
              flex items-center gap-5 flex-wrap">
    <!-- Avatar -->
    <div class="w-16 h-16 rounded-full flex items-center justify-center
                font-serif text-2xl font-bold text-white flex-shrink-0 shadow-lg"
      style="background: linear-gradient(135deg, #005A3C 0%, #007A52 100%)">
      {{ initials }}
    </div>
    <div class="flex-1 min-w-0">
      <h2 class="font-serif text-xl font-bold text-[#1A2E22] truncate">
        {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
        <span v-if="!authStore.user?.first_name" class="text-gray-400 font-sans font-normal text-base">
          {{ authStore.user?.username }}
        </span>
      </h2>
      <div class="flex items-center gap-2 flex-wrap mt-1">
        <span class="text-sm text-gray-500">@{{ authStore.user?.username }}</span>
        <span class="text-gray-300">·</span>
        <span class="text-xs font-bold px-2 py-0.5 rounded-full"
          :style="{ backgroundColor: role.bg, color: role.color }">
          {{ role.text }}
        </span>
      </div>
    </div>
    <div class="text-right text-xs text-gray-400">
      <div>{{ authStore.user?.nombre_declarations || 0 }} déclaration(s)</div>
      <div class="mt-0.5">Membre depuis {{ authStore.user?.date_creation
        ? new Date(authStore.user.date_creation).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
        : '—' }}</div>
    </div>
  </div>

  <!-- ══ Onglets ══ -->
  <div class="flex gap-1 bg-white rounded-xl p-1 border border-gray-200 shadow-sm mb-5 w-fit">
    <button v-for="t in [
      { key: 'info',     label: '✏️ Informations' },
      { key: 'password', label: '🔐 Mot de passe' },
    ]" :key="t.key"
      @click="tab = t.key; clearMessages()"
      :class="[
        'text-xs font-semibold px-4 py-2 rounded-lg transition-all cursor-pointer border-none',
        tab === t.key
          ? 'bg-[#005A3C] text-white shadow-sm'
          : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
      ]">
      {{ t.label }}
    </button>
  </div>

  <!-- ══ Feedback ══ -->
  <transition name="slide-msg">
    <div v-if="success"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      <span>✅</span><span>{{ success }}</span>
      <button @click="success = null" class="ml-auto bg-transparent border-none cursor-pointer text-green-400 hover:text-green-600">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️</span><span>{{ apiError }}</span>
      <button @click="apiError = null" class="ml-auto bg-transparent border-none cursor-pointer text-red-300 hover:text-rouge">✕</button>
    </div>
  </transition>

  <!-- ══ Onglet Informations ══ -->
  <transition name="fade-tab" mode="out-in">
  <div v-if="tab === 'info'" key="info" class="bg-white rounded-2xl shadow-card border border-gray-100 p-6">
    <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
      <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">✏️</span>
      Informations personnelles
    </h2>

    <form @submit.prevent="saveInfo" novalidate class="space-y-4">

      <!-- Prénom / Nom -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="form-label">Prénom</label>
          <input v-model="form.first_name" type="text"
            placeholder="Jean" class="form-input"/>
        </div>
        <div>
          <label class="form-label">Nom de famille</label>
          <input v-model="form.last_name" type="text"
            placeholder="AKODJO" class="form-input"/>
        </div>
      </div>

      <!-- Email -->
      <div>
        <label class="form-label">Adresse email</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✉️</span>
          <input v-model="form.email" type="email"
            placeholder="jean@example.tg"
            :class="['form-input pl-10', infoErrors.email && 'border-rouge ring-2 ring-rouge/15']"/>
        </div>
        <p v-if="infoErrors.email" class="form-error"><span>✕</span> {{ infoErrors.email }}</p>
      </div>

      <!-- Téléphone -->
      <div>
        <label class="form-label">Numéro de téléphone</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-sm">🇹🇬</span>
          <input v-model="form.telephone" type="tel"
            placeholder="+22890123456"
            :class="['form-input pl-10', infoErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"/>
        </div>
        <p v-if="infoErrors.telephone" class="form-error"><span>✕</span> {{ infoErrors.telephone }}</p>
      </div>

      <!-- Username (readonly) -->
      <div>
        <label class="form-label">Nom d'utilisateur <span class="text-gray-400 normal-case font-normal">(non modifiable)</span></label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">@</span>
          <input :value="authStore.user?.username" type="text"
            disabled class="form-input pl-8 bg-gray-50 text-gray-400 cursor-not-allowed"/>
        </div>
      </div>

      <!-- Bouton -->
      <div class="flex items-center justify-end pt-2">
        <button type="submit" :disabled="submitting"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>💾</span>
          {{ submitting ? 'Enregistrement…' : 'Enregistrer' }}
        </button>
      </div>

    </form>
  </div>
  </transition>

  <!-- ══ Onglet Mot de passe ══ -->
  <transition name="fade-tab" mode="out-in">
  <div v-if="tab === 'password'" key="password" class="bg-white rounded-2xl shadow-card border border-gray-100 p-6">
    <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
      <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">🔐</span>
      Changer le mot de passe
    </h2>

    <form @submit.prevent="savePassword" novalidate class="space-y-4">

      <div v-for="field in [
        { key: 'current', model: 'current_password', label: 'Mot de passe actuel',    show: 'current' },
        { key: 'new',     model: 'new_password',     label: 'Nouveau mot de passe',   show: 'new'     },
        { key: 'confirm', model: 'confirm_password', label: 'Confirmer le mot de passe', show: 'confirm' },
      ]" :key="field.key">
        <label class="form-label">{{ field.label }}</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
          <input v-model="pwdForm[field.model]"
            :type="showPwd[field.show] ? 'text' : 'password'"
            :placeholder="field.label"
            :class="['form-input pl-10 pr-12', pwdErrors[field.key] && 'border-rouge ring-2 ring-rouge/15']"/>
          <button type="button"
            @click="showPwd[field.show] = !showPwd[field.show]"
            class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                   hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
            {{ showPwd[field.show] ? '🙈' : '👁️' }}
          </button>
        </div>
        <p v-if="pwdErrors[field.key]" class="form-error"><span>✕</span> {{ pwdErrors[field.key] }}</p>
      </div>

      <!-- Critères -->
      <ul class="text-xs bg-gray-50 rounded-xl p-3 space-y-1 list-none pl-0">
        <li v-for="rule in [
          { ok: pwdForm.new_password.length >= 8,            text: 'Minimum 8 caractères' },
          { ok: /[A-Z]/.test(pwdForm.new_password),          text: 'Au moins une majuscule' },
          { ok: /[0-9]/.test(pwdForm.new_password),          text: 'Au moins un chiffre' },
          { ok: pwdForm.new_password === pwdForm.confirm_password && pwdForm.new_password.length > 0,
            text: 'Mots de passe identiques' },
        ]" :key="rule.text"
          :class="['flex items-center gap-2', rule.ok ? 'text-[#005A3C]' : 'text-gray-400']">
          <span>{{ rule.ok ? '✓' : '○' }}</span> {{ rule.text }}
        </li>
      </ul>

      <div class="flex items-center justify-end pt-2">
        <button type="submit" :disabled="submitting"
          class="flex items-center gap-2 bg-[#C41230] text-white font-bold
                 text-sm px-6 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>🔐</span>
          {{ submitting ? 'Mise à jour…' : 'Changer le mot de passe' }}
        </button>
      </div>

    </form>
  </div>
  </transition>

  <!-- ══ Zone danger ══ -->
  <div class="mt-5 bg-white rounded-2xl shadow-card border border-gray-100 p-5">
    <h3 class="font-serif text-sm font-bold text-rouge mb-3">Zone de déconnexion</h3>
    <p class="text-xs text-gray-500 mb-3">
      Votre session sera terminée et vous serez redirigé vers la page d'accueil.
    </p>
    <button @click="authStore.logout()"
      class="flex items-center gap-2 bg-red-50 text-rouge font-semibold
             text-xs px-5 py-2.5 rounded-xl border border-red-200
             cursor-pointer hover:bg-red-100 transition-all">
      🚪 Se déconnecter
    </button>
  </div>

</div>
</div>
</template>

<style scoped>
.fade-tab-enter-active, .fade-tab-leave-active { transition: all .2s ease; }
.fade-tab-enter-from, .fade-tab-leave-to { opacity: 0; transform: translateX(10px); }
.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-6px); }
.loader-dot {
  display: inline-block; width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>