<script setup>
import { ref, computed, onMounted } from 'vue'
import { usersAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

/* ══ État principal ══ */
const users      = ref([])
const loading    = ref(true)
const apiError   = ref(null)
const apiSuccess = ref(null)

/* ══ Filtres ══ */
const filterRole = ref('')        // '' | 'citoyen' | 'police' | 'admin'
const search     = ref('')

/* ══ Modale confirmation suppression ══ */
const confirmModal  = ref(false)
const userToDelete  = ref(null)
const deleting      = ref(false)

/* ══ Chargement ══ */
onMounted(loadUsers)

async function loadUsers() {
  loading.value  = true
  apiError.value = null
  try {
    const { data } = await usersAPI.list()
    users.value = data
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Impossible de charger les utilisateurs.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage côté client ══ */
const filtered = computed(() => {
  let list = users.value

  if (filterRole.value) {
    list = list.filter(u => u.role === filterRole.value)
  }

  const q = search.value.toLowerCase().trim()
  if (q) {
    list = list.filter(u =>
      u.username.toLowerCase().includes(q)          ||
      (u.first_name || '').toLowerCase().includes(q) ||
      (u.last_name  || '').toLowerCase().includes(q) ||
      (u.email      || '').toLowerCase().includes(q)
    )
  }
  return list
})

/* ══ Stats rapides ══ */
const stats = computed(() => ({
  total:    users.value.length,
  citoyens: users.value.filter(u => u.role === 'citoyen').length,
  police:   users.value.filter(u => u.role === 'police').length,
  admins:   users.value.filter(u => u.role === 'admin').length,
  actifs:   users.value.filter(u => u.is_active).length,
}))

/* ══ Suppression ══ */
function askDelete(user) {
  userToDelete.value = user
  confirmModal.value = true
}

async function confirmDelete() {
  if (!userToDelete.value) return
  deleting.value = true
  apiError.value = null
  try {
    await usersAPI.delete(userToDelete.value.id)
    users.value    = users.value.filter(u => u.id !== userToDelete.value.id)
    apiSuccess.value = `✅ L'utilisateur « ${userToDelete.value.username} » a été supprimé.`
    confirmModal.value  = false
    userToDelete.value  = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la suppression.'
  } finally {
    deleting.value = false
  }
}

/* ══ Helpers ══ */
const roleConfig = {
  citoyen: { label: 'Citoyen',       icon: '👤', color: '#059669', bg: '#D1FAE5' },
  police:  { label: 'Agent police',  icon: '👮', color: '#2563EB', bg: '#DBEAFE' },
  admin:   { label: 'Administrateur',icon: '🛡️', color: '#C41230', bg: '#FEE2E2' },
}
const getRole = (r) => roleConfig[r] || roleConfig.citoyen

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const initiales = (u) =>
  u.first_name && u.last_name
    ? (u.first_name[0] + u.last_name[0]).toUpperCase()
    : u.username[0].toUpperCase()

const avatarBg = (role) =>
  role === 'admin'   ? 'linear-gradient(135deg,#C41230,#8B0D22)' :
  role === 'police'  ? 'linear-gradient(135deg,#2563EB,#1e40af)' :
                       'linear-gradient(135deg,#059669,#065F46)'

const tabRoles = [
  { value: '',        label: 'Tous',    emoji: '👥' },
  { value: 'citoyen', label: 'Citoyens',emoji: '👤' },
  { value: 'police',  label: 'Agents',  emoji: '👮' },
  { value: 'admin',   label: 'Admins',  emoji: '🛡️' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-5xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🛡️ Réservé aux administrateurs
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des utilisateurs
      </h1>
      <p class="text-sm text-gray-500">
        Consultez et supprimez les comptes citoyens, agents et administrateurs.
      </p>
    </div>
    <router-link :to="{ name: 'dashboard' }"
      class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
             bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
             hover:bg-gray-50 transition-all self-start">
      ← Tableau de bord
    </router-link>
  </div>

  <!-- ══ Feedback ══ -->
  <transition name="slide-msg">
    <div v-if="apiSuccess"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      {{ apiSuccess }}
      <button @click="apiSuccess = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-green-400">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError && !confirmModal"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Compteurs ══ -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
    <div v-for="c in [
        { label:'Total',    val: stats.total,    icon:'👥', color:'#005A3C', bg:'#E8F4F0' },
        { label:'Citoyens', val: stats.citoyens, icon:'👤', color:'#059669', bg:'#D1FAE5' },
        { label:'Agents',   val: stats.police,   icon:'👮', color:'#2563EB', bg:'#DBEAFE' },
        { label:'Admins',   val: stats.admins,   icon:'🛡️', color:'#C41230', bg:'#FEE2E2' },
      ]" :key="c.label"
      class="bg-white rounded-2xl border border-gray-100 shadow-card p-4 flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg"
        :style="{ backgroundColor: c.bg }">{{ c.icon }}</div>
      <div>
        <div class="font-serif text-xl font-bold" :style="{ color: c.color }">{{ c.val }}</div>
        <div class="text-xs text-gray-400">{{ c.label }}</div>
      </div>
    </div>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-5">
    <!-- Tabs rôle -->
    <div class="flex items-center gap-1 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
      <button v-for="tab in tabRoles" :key="tab.value"
        @click="filterRole = tab.value"
        :class="[
          'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border-none cursor-pointer',
          filterRole === tab.value
            ? 'bg-[#005A3C] text-white shadow'
            : 'text-gray-500 hover:bg-gray-50 bg-transparent'
        ]">
        {{ tab.emoji }} {{ tab.label }}
      </button>
    </div>
    <!-- Recherche -->
    <div class="relative flex-1">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher par nom, username, email…"
        class="form-input pl-10 text-sm w-full" />
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">🔍</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-1">Aucun résultat</p>
    <p class="text-sm text-gray-400">Modifiez vos filtres ou votre recherche.</p>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="user in filtered" :key="user.id"
        :class="[
          'bg-white rounded-2xl border shadow-card transition-all',
          !user.is_active ? 'opacity-60 border-red-200' : 'border-gray-100'
        ]">
        <div class="p-4 flex items-center gap-4 flex-wrap">

          <!-- Avatar -->
          <div class="w-10 h-10 rounded-full flex items-center justify-center
                      font-serif font-bold text-white text-sm flex-shrink-0 shadow"
            :style="{ background: avatarBg(user.role) }">
            {{ initiales(user) }}
          </div>

          <!-- Infos -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-0.5">
              <span class="font-semibold text-sm text-[#1A2E22]">
                {{ user.first_name }} {{ user.last_name }}
              </span>
              <span class="text-xs text-gray-400">@{{ user.username }}</span>
              <span class="badge text-[10px] font-bold"
                :style="{ color: getRole(user.role).color, backgroundColor: getRole(user.role).bg }">
                {{ getRole(user.role).icon }} {{ getRole(user.role).label }}
              </span>
              <span v-if="!user.is_active"
                class="badge text-[10px] bg-red-100 text-rouge font-bold">
                ⛔ Désactivé
              </span>
              <!-- Badge "Vous" -->
              <span v-if="user.id === authStore.user?.id"
                class="badge text-[10px] bg-yellow-100 text-yellow-700 font-bold">
                ⭐ Vous
              </span>
            </div>
            <div class="flex items-center gap-3 text-[10px] text-gray-400 flex-wrap">
              <span v-if="user.email">✉️ {{ user.email }}</span>
              <span v-if="user.telephone">📞 {{ user.telephone }}</span>
              <span>📅 {{ formatDate(user.date_creation) }}</span>
              <span>📋 {{ user.nombre_declarations || 0 }} décl.</span>
            </div>
          </div>

          <!-- Action suppression -->
          <div class="flex-shrink-0">
            <button
              v-if="user.id !== authStore.user?.id"
              @click="askDelete(user)"
              class="inline-flex items-center gap-1.5 text-xs font-semibold
                     text-rouge bg-red-50 hover:bg-red-100 px-3 py-2 rounded-lg
                     border-none cursor-pointer transition-all">
              🗑️ Supprimer
            </button>
            <span v-else class="text-xs text-gray-300 bg-gray-50 px-3 py-2 rounded-lg">
              Votre compte
            </span>
          </div>

        </div>

        <!-- Barre colorée bas -->
        <div class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getRole(user.role).color, opacity: 0.25 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════════════
     MODALE — Confirmation suppression
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="confirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.5)"
    @click.self="confirmModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">

      <!-- Icône danger -->
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center
                  text-3xl mx-auto mb-4">
        🗑️
      </div>

      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Supprimer cet utilisateur ?
      </h3>

      <!-- Carte récap utilisateur -->
      <div v-if="userToDelete"
        class="flex items-center gap-3 bg-gray-50 rounded-xl p-3 mb-3 text-left">
        <div class="w-9 h-9 rounded-full flex items-center justify-center
                    font-bold text-white text-sm flex-shrink-0"
          :style="{ background: avatarBg(userToDelete.role) }">
          {{ initiales(userToDelete) }}
        </div>
        <div class="min-w-0">
          <p class="font-semibold text-sm text-[#1A2E22] truncate">
            {{ userToDelete.first_name }} {{ userToDelete.last_name }}
          </p>
          <p class="text-xs text-gray-400">@{{ userToDelete.username }} ·
            {{ getRole(userToDelete.role).label }}
          </p>
        </div>
      </div>

      <div class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-5 text-left">
        ⚠️ <strong>Action irréversible.</strong> Toutes les déclarations et notifications
        associées à ce compte seront également supprimées.
      </div>

      <!-- Erreur inline -->
      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        {{ apiError }}
      </div>

      <div class="flex gap-3">
        <button @click="confirmModal = false; apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDelete" :disabled="deleting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] disabled:opacity-50">
          <span v-if="deleting" class="loader"></span>
          <span v-else>🗑️</span>
          {{ deleting ? 'Suppression…' : 'Supprimer' }}
        </button>
      </div>
    </div>
  </div>
</transition>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .2s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(6px); }
.list-item-leave-active { transition: all .2s ease; position: absolute; width: 100%; }
.list-item-leave-to     { opacity: 0; transform: translateX(20px); }

.modal-enter-active, .modal-leave-active { transition: all .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: transform .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-5px); }

.loader {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>