<script setup>
import { ref, computed, onMounted } from 'vue'
import { agentsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router    = useRouter()

/* ══ État ══ */
const agents     = ref([])
const loading    = ref(true)
const apiError   = ref(null)
const apiSuccess = ref(null)
const search     = ref('')

/* ══ Modal création ══ */
const showCreate  = ref(false)
const submitting  = ref(false)
const form = ref({
  username:         '',
  first_name:       '',
  last_name:        '',
  email:            '',
  telephone:        '',
  role:             'police',
  password:         '',
  password_confirm: '',
})
const formErrors  = ref({})
const showPwd     = ref(false)
const showPwdConf = ref(false)

/* ══ Modal désactivation ══ */
const confirmModal = ref(false)
const agentToDeactivate = ref(null)
const deactivating = ref(false)

/* ══ Chargement ══ */
onMounted(loadAgents)

async function loadAgents() {
  loading.value   = true
  apiError.value  = null
  try {
    const { data } = await agentsAPI.list()
    agents.value   = data
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Impossible de charger les agents.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage ══ */
const filtered = computed(() => {
  const q = search.value.toLowerCase().trim()
  if (!q) return agents.value
  return agents.value.filter(a =>
    a.username.toLowerCase().includes(q)       ||
    (a.first_name || '').toLowerCase().includes(q) ||
    (a.last_name  || '').toLowerCase().includes(q) ||
    (a.email      || '').toLowerCase().includes(q)
  )
})

/* ══ Validation formulaire ══ */
function validateForm() {
  const e = {}
  if (!form.value.username.trim())   e.username   = "Nom d'utilisateur requis"
  if (form.value.username.trim().length < 3) e.username = 'Minimum 3 caractères'
  if (!/^[a-zA-Z0-9@.+\-_]+$/.test(form.value.username))
    e.username = 'Caractères invalides'
  if (!form.value.first_name.trim()) e.first_name = 'Prénom requis'
  if (!form.value.last_name.trim())  e.last_name  = 'Nom requis'
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"
  if (form.value.password.length < 8)      e.password = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(form.value.password))  e.password = 'Au moins une majuscule'
  if (!/[0-9]/.test(form.value.password))  e.password = 'Au moins un chiffre'
  if (form.value.password !== form.value.password_confirm)
    e.password_confirm = 'Les mots de passe ne correspondent pas'
  formErrors.value = e
  return Object.keys(e).length === 0
}

/* ══ Créer un agent ══ */
async function handleCreate() {
  if (!validateForm()) return
  submitting.value = true
  apiError.value   = null
  try {
    const { data } = await agentsAPI.create(form.value)
    agents.value.unshift(data.agent)
    apiSuccess.value = `✅ Agent "${data.agent.username}" créé avec succès.`
    resetForm()
    showCreate.value = false
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    const d = e.response?.data
    if (typeof d === 'object') {
      // Erreurs de champs → afficher dans le formulaire
      formErrors.value = d
      apiError.value = 'Veuillez corriger les erreurs ci-dessous.'
    } else {
      apiError.value = d || 'Erreur lors de la création.'
    }
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = {
    username: '', first_name: '', last_name: '',
    email: '', telephone: '', role: 'police',
    password: '', password_confirm: '',
  }
  formErrors.value = {}
  showPwd.value = false
  showPwdConf.value = false
}

/* ══ Désactiver un agent ══ */
function askDeactivate(agent) {
  agentToDeactivate.value = agent
  confirmModal.value = true
}

async function confirmDeactivate() {
  if (!agentToDeactivate.value) return
  deactivating.value = true
  apiError.value     = null
  try {
    await agentsAPI.delete(agentToDeactivate.value.id)
    // Marquer comme inactif dans la liste locale
    const idx = agents.value.findIndex(a => a.id === agentToDeactivate.value.id)
    if (idx !== -1) agents.value[idx].is_active = false
    apiSuccess.value = `Le compte de "${agentToDeactivate.value.username}" a été désactivé.`
    confirmModal.value = false
    agentToDeactivate.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la désactivation.'
  } finally {
    deactivating.value = false
  }
}

/* ══ Réactiver un agent ══ */
async function reactivate(agent) {
  apiError.value = null
  try {
    await agentsAPI.update(agent.id, { is_active: true })
    const idx = agents.value.findIndex(a => a.id === agent.id)
    if (idx !== -1) agents.value[idx].is_active = true
    apiSuccess.value = `Le compte de "${agent.username}" a été réactivé.`
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la réactivation.'
  }
}

/* ══ Helpers ══ */
const roleConfig = {
  admin:  { label: 'Administrateur', icon: '🛡️', color: '#C41230', bg: '#FEE2E2' },
  police: { label: 'Agent de police', icon: '👮', color: '#2563EB', bg: '#DBEAFE' },
}
const getRole = (r) => roleConfig[r] || roleConfig.police

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const initiales = (a) => {
  if (a.first_name && a.last_name)
    return (a.first_name[0] + a.last_name[0]).toUpperCase()
  return a.username[0].toUpperCase()
}
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-4xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🛡️ Réservé aux administrateurs
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des agents
      </h1>
      <p class="text-sm text-gray-500">
        Créez et gérez les comptes des agents de police et des administrateurs.
      </p>
    </div>
    <div class="flex items-center gap-2">
      <router-link :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
               bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
               hover:bg-gray-50 transition-all">
        ← Tableau de bord
      </router-link>
      <button @click="showCreate = true"
        class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
               text-sm px-5 py-2.5 rounded-xl border-none cursor-pointer
               hover:bg-[#007A52] hover:-translate-y-0.5 transition-all shadow-md">
        + Créer un agent
      </button>
    </div>
  </div>

  <!-- ══ Feedback global ══ -->
  <transition name="slide-msg">
    <div v-if="apiSuccess"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      <span>{{ apiSuccess }}</span>
      <button @click="apiSuccess = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-green-400">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError && !showCreate"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️ {{ apiError }}</span>
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Barre de recherche + stats ══ -->
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-5">
    <div class="relative flex-1">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher un agent par nom, prénom, username…"
        class="form-input pl-10 text-sm w-full"/>
    </div>
    <div class="flex items-center gap-3 text-xs text-gray-500 bg-white px-4 py-2.5
                rounded-xl border border-gray-200 shadow-sm flex-shrink-0">
      <span>👮 <strong class="text-[#2563EB]">{{ agents.filter(a => a.role === 'police').length }}</strong> agents</span>
      <span class="text-gray-300">·</span>
      <span>🛡️ <strong class="text-[#C41230]">{{ agents.filter(a => a.role === 'admin').length }}</strong> admins</span>
      <span class="text-gray-300">·</span>
      <span>✅ <strong class="text-[#005A3C]">{{ agents.filter(a => a.is_active).length }}</strong> actifs</span>
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Liste vide ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">👤</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-2">Aucun agent trouvé</p>
    <p class="text-sm text-gray-500 mb-4">
      {{ search ? 'Aucun résultat pour cette recherche.' : 'Créez le premier agent.' }}
    </p>
    <button v-if="!search" @click="showCreate = true"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-5 py-2.5 rounded-xl border-none cursor-pointer
             hover:bg-[#007A52] transition-all">
      + Créer un agent
    </button>
  </div>

  <!-- ══ Liste des agents ══ -->
  <div v-else class="space-y-3">
    <transition-group name="list-item">
      <div v-for="agent in filtered" :key="agent.id"
        :class="[
          'bg-white rounded-2xl border shadow-card transition-all',
          !agent.is_active && 'opacity-60'
        ]"
        :style="{ borderColor: agent.is_active ? '#e5e7eb' : '#fca5a5' }">

        <div class="p-5 flex items-center gap-4 flex-wrap">

          <!-- Avatar initiales -->
          <div class="w-11 h-11 rounded-full flex items-center justify-center
                      font-serif font-bold text-white text-sm flex-shrink-0 shadow"
            :style="{
              background: agent.role === 'admin'
                ? 'linear-gradient(135deg,#C41230,#8B0D22)'
                : 'linear-gradient(135deg,#2563EB,#1e40af)'
            }">
            {{ initiales(agent) }}
          </div>

          <!-- Infos principales -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-0.5">
              <span class="font-semibold text-sm text-[#1A2E22]">
                {{ agent.first_name }} {{ agent.last_name }}
              </span>
              <span class="text-xs text-gray-400">@{{ agent.username }}</span>
              <!-- Badge rôle -->
              <span class="badge text-[10px] font-bold"
                :style="{
                  color: getRole(agent.role).color,
                  backgroundColor: getRole(agent.role).bg
                }">
                {{ getRole(agent.role).icon }} {{ getRole(agent.role).label }}
              </span>
              <!-- Badge inactif -->
              <span v-if="!agent.is_active"
                class="badge text-[10px] bg-red-100 text-rouge font-bold">
                ⛔ Désactivé
              </span>
            </div>
            <div class="flex items-center gap-3 text-xs text-gray-400 flex-wrap">
              <span v-if="agent.email">✉️ {{ agent.email }}</span>
              <span v-if="agent.telephone">📞 {{ agent.telephone }}</span>
              <span>📅 Créé le {{ formatDate(agent.date_creation) }}</span>
              <span>📋 {{ agent.nombre_declarations || 0 }} déclaration(s)</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Empêcher de se modifier soi-même -->
            <template v-if="agent.id !== authStore.user?.id">
              <button v-if="agent.is_active"
                @click="askDeactivate(agent)"
                class="text-xs font-semibold text-rouge bg-red-50 hover:bg-red-100
                       px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
                ⛔ Désactiver
              </button>
              <button v-else
                @click="reactivate(agent)"
                class="text-xs font-semibold text-green-700 bg-green-50 hover:bg-green-100
                       px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
                ✅ Réactiver
              </button>
            </template>
            <!-- Compte courant — non modifiable -->
            <span v-else
              class="text-xs text-gray-400 bg-gray-100 px-3 py-2 rounded-lg">
              Votre compte
            </span>
          </div>

        </div>

        <!-- Barre colorée -->
        <div class="h-0.5 rounded-b-2xl"
          :style="{
            backgroundColor: agent.is_active ? getRole(agent.role).color : '#fca5a5',
            opacity: 0.35
          }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ═══════════════════════════════════════════
     MODAL — Créer un agent
═══════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="showCreate"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto"
    style="background:rgba(0,0,0,.45)"
    @click.self="showCreate = false; resetForm(); apiError = null">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-4 relative">

      <!-- En-tête modal -->
      <div class="flex items-center justify-between p-6 border-b border-gray-100">
        <div>
          <h2 class="font-serif text-xl font-bold text-[#1A2E22]">Créer un agent</h2>
          <p class="text-xs text-gray-500 mt-0.5">
            Le compte sera immédiatement actif. Communiquez le mot de passe à l'agent.
          </p>
        </div>
        <button @click="showCreate = false; resetForm(); apiError = null"
          class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center
                 text-gray-500 border-none cursor-pointer hover:bg-gray-200 transition-all">
          ✕
        </button>
      </div>

      <div class="p-6 space-y-4">

        <!-- Erreur globale -->
        <div v-if="apiError"
          class="flex items-center gap-2 bg-red-50 border border-red-200
                 rounded-xl p-3 text-sm text-rouge">
          <span>⚠️</span><span>{{ apiError }}</span>
        </div>

        <!-- Choix du rôle -->
        <div>
          <label class="form-label">Rôle <span class="text-rouge">*</span></label>
          <div class="grid grid-cols-2 gap-3">
            <button type="button"
              @click="form.role = 'police'"
              :class="[
                'flex items-center gap-3 p-3.5 rounded-xl border-2 text-left transition-all cursor-pointer',
                form.role === 'police'
                  ? 'border-[#2563EB] bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-blue-200'
              ]">
              <span class="text-2xl">👮</span>
              <div>
                <div class="font-semibold text-sm text-[#1A2E22]">Agent de police</div>
                <div class="text-xs text-gray-500">Valide les déclarations</div>
              </div>
            </button>
            <button type="button"
              @click="form.role = 'admin'"
              :class="[
                'flex items-center gap-3 p-3.5 rounded-xl border-2 text-left transition-all cursor-pointer',
                form.role === 'admin'
                  ? 'border-[#C41230] bg-red-50'
                  : 'border-gray-200 bg-white hover:border-red-200'
              ]">
              <span class="text-2xl">🛡️</span>
              <div>
                <div class="font-semibold text-sm text-[#1A2E22]">Administrateur</div>
                <div class="text-xs text-gray-500">Accès complet</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Prénom + Nom -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="form-label">Prénom <span class="text-rouge">*</span></label>
            <input v-model="form.first_name" type="text" placeholder="Jean"
              :class="['form-input', formErrors.first_name && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.first_name" class="form-error text-xs mt-1">
              ✕ {{ formErrors.first_name }}
            </p>
          </div>
          <div>
            <label class="form-label">Nom <span class="text-rouge">*</span></label>
            <input v-model="form.last_name" type="text" placeholder="KOFFI"
              :class="['form-input', formErrors.last_name && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.last_name" class="form-error text-xs mt-1">
              ✕ {{ formErrors.last_name }}
            </p>
          </div>
        </div>

        <!-- Username -->
        <div>
          <label class="form-label">
            Nom d'utilisateur <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">@</span>
            <input v-model="form.username" type="text" placeholder="agent_koffi"
              :class="['form-input pl-8', formErrors.username && 'border-rouge ring-2 ring-rouge/15']"/>
          </div>
          <p v-if="formErrors.username" class="form-error text-xs mt-1">
            ✕ {{ formErrors.username }}
          </p>
        </div>

        <!-- Email + Téléphone -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="form-label">
              Email <span class="text-gray-400 normal-case font-normal">(opt.)</span>
            </label>
            <input v-model="form.email" type="email" placeholder="agent@police.tg"
              :class="['form-input', formErrors.email && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.email" class="form-error text-xs mt-1">✕ {{ formErrors.email }}</p>
          </div>
          <div>
            <label class="form-label">
              Téléphone <span class="text-gray-400 normal-case font-normal">(opt.)</span>
            </label>
            <input v-model="form.telephone" type="tel" placeholder="+22890000000"
              :class="['form-input', formErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.telephone" class="form-error text-xs mt-1">✕ {{ formErrors.telephone }}</p>
          </div>
        </div>

        <!-- Mot de passe -->
        <div>
          <label class="form-label">
            Mot de passe initial <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
            <input v-model="form.password"
              :type="showPwd ? 'text' : 'password'"
              placeholder="Min. 8 car., 1 majuscule, 1 chiffre"
              :class="['form-input pl-10 pr-12', formErrors.password && 'border-rouge ring-2 ring-rouge/15']"/>
            <button type="button" @click="showPwd = !showPwd"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                     bg-transparent border-none cursor-pointer hover:text-gray-600">
              {{ showPwd ? '🙈' : '👁️' }}
            </button>
          </div>
          <p v-if="formErrors.password" class="form-error text-xs mt-1">✕ {{ formErrors.password }}</p>
        </div>

        <!-- Confirmation mot de passe -->
        <div>
          <label class="form-label">
            Confirmer le mot de passe <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔑</span>
            <input v-model="form.password_confirm"
              :type="showPwdConf ? 'text' : 'password'"
              placeholder="Répétez le mot de passe"
              :class="['form-input pl-10 pr-12', formErrors.password_confirm && 'border-rouge ring-2 ring-rouge/15']"/>
            <button type="button" @click="showPwdConf = !showPwdConf"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                     bg-transparent border-none cursor-pointer hover:text-gray-600">
              {{ showPwdConf ? '🙈' : '👁️' }}
            </button>
          </div>
          <p v-if="formErrors.password_confirm" class="form-error text-xs mt-1">
            ✕ {{ formErrors.password_confirm }}
          </p>
          <p v-else-if="form.password && form.password === form.password_confirm"
            class="text-xs text-green-600 mt-1">✓ Les mots de passe correspondent</p>
        </div>

        <!-- Note sécurité -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-3 text-xs text-yellow-700">
          ⚠️ <strong>Important :</strong> Communiquez ce mot de passe à l'agent de manière sécurisée.
          Il pourra le modifier depuis son profil.
        </div>

      </div>

      <!-- Pied de modal -->
      <div class="flex gap-3 p-6 border-t border-gray-100">
        <button type="button"
          @click="showCreate = false; resetForm(); apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 transition-all cursor-pointer">
          Annuler
        </button>
        <button type="button"
          @click="handleCreate"
          :disabled="submitting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed"
          :style="{
            backgroundColor: form.role === 'admin' ? '#C41230' : '#005A3C'
          }">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>{{ form.role === 'admin' ? '🛡️' : '👮' }}</span>
          {{ submitting ? 'Création…' : 'Créer l\'agent' }}
        </button>
      </div>

    </div>
  </div>
</transition>

<!-- ═══════════════════════════════════════════
     MODAL — Confirmation désactivation
═══════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="confirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.45)"
    @click.self="confirmModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">
      <div class="text-4xl mb-3">⚠️</div>
      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Désactiver cet agent ?
      </h3>
      <p class="text-sm text-gray-500 mb-1">
        Le compte de
        <strong>{{ agentToDeactivate?.first_name }} {{ agentToDeactivate?.last_name }}</strong>
        sera désactivé.
      </p>
      <p class="text-xs text-gray-400 mb-6">
        L'agent ne pourra plus se connecter. Vous pourrez le réactiver ultérieurement.
      </p>
      <div class="flex gap-3">
        <button @click="confirmModal = false"
          class="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDeactivate"
          :disabled="deactivating"
          class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] disabled:opacity-50">
          <span v-if="deactivating" class="loader-dot"></span>
          <span v-else>⛔</span>
          {{ deactivating ? 'En cours…' : 'Désactiver' }}
        </button>
      </div>
    </div>

  </div>
</transition>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(8px); }

.modal-enter-active, .modal-leave-active { transition: all .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: all .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-6px); }

.loader-dot {
  display: inline-block; width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-error { @apply text-rouge text-xs flex items-center gap-1; }
</style>