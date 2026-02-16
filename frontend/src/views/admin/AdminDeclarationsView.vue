<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declarations = ref([])
const loading      = ref(true)
const apiError     = ref(null)
const apiSuccess   = ref(null)
const search       = ref('')
const filterStatut = ref('')
const filterType   = ref('')

/* ══ Modale changement de statut ══ */
const statutModal    = ref(false)
const selectedDecl   = ref(null)
const nouveauStatut  = ref('')
const remarques      = ref('')
const changingStatut = ref(false)

/* ══ Modale suppression ══ */
const deleteModal  = ref(false)
const declToDelete = ref(null)
const deleting     = ref(false)

/* ══ Chargement ══ */
onMounted(loadDeclarations)

async function loadDeclarations() {
  loading.value  = true
  apiError.value = null
  try {
    const { data } = await declarationsAPI.list()
    // ✅ CORRECTION : L'API Django retourne un objet paginé avec 'results'
    declarations.value = data.results ?? data
    console.log('✅ Déclarations chargées:', declarations.value.length)
  } catch (e) {
    apiError.value = 'Impossible de charger les déclarations.'
    console.error('❌ Erreur chargement déclarations:', e)
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage AMÉLIORÉ ══ */
const filtered = computed(() => {
  let list = declarations.value

  // Filtre par statut
  if (filterStatut.value) {
    list = list.filter(d => d.statut === filterStatut.value)
  }

  // Filtre par type
  if (filterType.value) {
    list = list.filter(d => d.type_declaration === filterType.value)
  }

  // Recherche textuelle améliorée
  const q = search.value.toLowerCase().trim()
  if (q) {
    list = list.filter(d => {
      // Normaliser pour la recherche (gérer les espaces multiples, etc.)
      const normalizeText = (text) => {
        return (text || '').toLowerCase().trim().replace(/\s+/g, ' ')
      }

      // Champs de recherche
      const numeroPiece   = normalizeText(d.numero_piece)
      const nomSurPiece   = normalizeText(d.nom_sur_piece)
      const numeroRecep   = normalizeText(d.numero_recepisse)
      const declarant     = normalizeText(d.declarant)
      const nomDeclarant  = normalizeText(d.nom_declarant)
      const prenomDecl    = normalizeText(d.prenom_declarant)
      const categorie     = normalizeText(d.categorie_nom)
      const lieuPerte     = normalizeText(d.lieu_perte)

      // Recherche dans tous les champs pertinents
      return numeroPiece.includes(q)   ||
             nomSurPiece.includes(q)   ||
             numeroRecep.includes(q)   ||
             declarant.includes(q)     ||
             nomDeclarant.includes(q)  ||
             prenomDecl.includes(q)    ||
             categorie.includes(q)     ||
             lieuPerte.includes(q)
    })
  }

  return list
})

/* ══ Changement de statut ══ */
function openStatut(decl) {
  selectedDecl.value  = decl
  nouveauStatut.value = decl.statut
  remarques.value     = ''
  statutModal.value   = true
}

async function handleChangerStatut() {
  if (!selectedDecl.value) return
  changingStatut.value = true
  apiError.value       = null
  try {
    const { data } = await declarationsAPI.changerStatut(selectedDecl.value.id, {
      statut: nouveauStatut.value,
      remarques: remarques.value,
    })
    const idx = declarations.value.findIndex(d => d.id === data.id)
    if (idx !== -1) {
      declarations.value[idx].statut        = data.statut
      declarations.value[idx].statut_display = data.statut_display
    }
    apiSuccess.value  = `✅ Statut mis à jour pour ${selectedDecl.value.numero_recepisse}`
    statutModal.value = false
    selectedDecl.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors du changement de statut.'
  } finally {
    changingStatut.value = false
  }
}

/* ══ Suppression ══ */
function askDelete(decl) {
  declToDelete.value = decl
  deleteModal.value  = true
}

async function confirmDelete() {
  if (!declToDelete.value) return
  deleting.value = true
  apiError.value = null
  try {
    await declarationsAPI.delete(declToDelete.value.id)
    declarations.value = declarations.value.filter(d => d.id !== declToDelete.value.id)
    apiSuccess.value = `✅ Déclaration « ${declToDelete.value.numero_recepisse} » supprimée.`
    deleteModal.value  = false
    declToDelete.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la suppression.'
  } finally {
    deleting.value = false
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente', color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',     color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',   color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',   color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',     color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',    color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const statutOptions = Object.entries(statusConfig).map(([v, c]) => ({ value: v, label: c.label }))
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-6xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des déclarations
      </h1>
      <p class="text-sm text-gray-500">
        Validez, changez le statut ou supprimez des déclarations.
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
    <div v-if="apiError && !statutModal && !deleteModal"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Filtres AMÉLIORÉS ══ -->
  <div class="flex flex-wrap gap-3 mb-5">
    <!-- Recherche avec placeholder détaillé -->
    <div class="relative flex-1 min-w-[280px]">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher par N° pièce, nom, récépissé, déclarant, catégorie, lieu…"
        class="form-input pl-10 text-sm w-full" />
      <!-- Compteur de résultats -->
      <div v-if="search" class="absolute right-3 top-1/2 -translate-y-1/2">
        <span class="text-xs bg-[#E8F4F0] text-[#005A3C] px-2 py-1 rounded-full font-semibold">
          {{ filtered.length }}
        </span>
      </div>
    </div>
    
    <!-- Filtre type -->
    <select v-model="filterType" class="form-input text-sm w-auto min-w-[140px]">
      <option value="">Tous les types</option>
      <option value="PERTE">😟 Pertes</option>
      <option value="TROUVAILLE">🤲 Trouvailles</option>
    </select>
    
    <!-- Filtre statut -->
    <select v-model="filterStatut" class="form-input text-sm w-auto min-w-[160px]">
      <option value="">Tous les statuts</option>
      <option v-for="s in statutOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
    </select>
    
    <!-- Bouton réinitialiser filtres -->
    <button v-if="search || filterType || filterStatut"
      @click="search = ''; filterType = ''; filterStatut = ''"
      class="text-xs text-gray-400 hover:text-rouge px-3 py-2 rounded-lg
             bg-white border border-gray-200 cursor-pointer transition-all hover:border-rouge/30">
      ✕ Réinitialiser
    </button>
  </div>

  <!-- Compteur résultats détaillé -->
  <div class="flex items-center justify-between mb-3">
    <p class="text-xs text-gray-500">
      <span class="font-bold text-[#005A3C]">{{ filtered.length }}</span> déclaration(s) affichée(s)
      <span v-if="filtered.length !== declarations.length" class="text-gray-400">
        sur {{ declarations.length }} au total
      </span>
    </p>
    
    <!-- Info recherche active -->
    <div v-if="search" class="text-xs text-gray-400 flex items-center gap-2">
      <span>🔍 Recherche active :</span>
      <span class="font-mono bg-gray-100 px-2 py-0.5 rounded text-[#005A3C]">{{ search }}</span>
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="skeleton h-24 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="filtered.length === 0 && declarations.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">📋</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-1">Aucune déclaration</p>
    <p class="text-sm text-gray-400">La base de données est vide.</p>
  </div>
  
  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500 mb-1">Aucune déclaration ne correspond aux critères</p>
    <p class="text-xs text-gray-400 mb-4">
      Essayez de modifier vos filtres ou votre recherche
    </p>
    <button @click="search = ''; filterType = ''; filterStatut = ''"
      class="text-xs text-[#005A3C] font-semibold bg-[#E8F4F0] px-4 py-2 rounded-lg
             border-none cursor-pointer hover:bg-[#d0ece3] transition-all">
      Réinitialiser les filtres
    </button>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="decl in filtered" :key="decl.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card transition-all">

        <div class="p-4 flex items-start gap-4 flex-wrap">

          <!-- Icône type -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
            :style="{
              backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
            }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>

          <!-- Infos déclaration -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-1">
              <span class="font-mono text-sm font-bold text-[#005A3C]">
                {{ decl.numero_recepisse }}
              </span>
              <span class="badge text-[10px] font-bold"
                :style="{ color: getStatus(decl.statut).color, backgroundColor: getStatus(decl.statut).bg }">
                {{ getStatus(decl.statut).label }}
              </span>
              <span class="badge text-[10px] font-semibold"
                :style="{
                  backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
                  color: decl.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
                }">
                {{ decl.type_display || decl.type_declaration }}
              </span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-x-4 gap-y-0.5 text-xs text-gray-500">
              <span>📄 {{ decl.numero_piece || '—' }}</span>
              <span>👤 {{ decl.nom_sur_piece || '—' }}</span>
              <span>👥 {{ decl.declarant || '—' }}</span>
              <span>📅 {{ formatDate(decl.date_declaration) }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Voir le détail -->
            <button @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
              class="text-xs font-semibold text-[#005A3C] bg-[#E8F4F0] hover:bg-[#c8e8dc]
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              👁️ Voir
            </button>
            <!-- Changer statut -->
            <button @click="openStatut(decl)"
              class="text-xs font-semibold text-[#2563EB] bg-blue-50 hover:bg-blue-100
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              ✏️ Statut
            </button>
            <!-- Supprimer — admin uniquement -->
            <button v-if="authStore.isAdmin"
              @click="askDelete(decl)"
              class="text-xs font-semibold text-rouge bg-red-50 hover:bg-red-100
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              🗑️ Supprimer
            </button>
          </div>
        </div>

        <div class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getStatus(decl.statut).color, opacity: 0.25 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════════════
     MODALE — Changer statut
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="statutModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.45)"
    @click.self="statutModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1">Changer le statut</h2>
      <p class="text-xs text-gray-400 mb-5">
        Déclaration : <strong class="font-mono">{{ selectedDecl?.numero_recepisse }}</strong>
      </p>

      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        ⚠️ {{ apiError }}
      </div>

      <div class="space-y-4">
        <div>
          <label class="form-label">Nouveau statut <span class="text-rouge">*</span></label>
          <select v-model="nouveauStatut" class="form-input text-sm">
            <option v-for="s in statutOptions" :key="s.value" :value="s.value">
              {{ s.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="form-label">Remarques <span class="text-gray-400 font-normal">(optionnel)</span></label>
          <textarea v-model="remarques" rows="3" placeholder="Informations complémentaires…"
            class="form-input text-sm resize-none"></textarea>
        </div>
      </div>

      <div class="flex gap-3 mt-5">
        <button @click="statutModal = false; apiError = null"
          class="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="handleChangerStatut" :disabled="changingStatut"
          class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl
                 bg-[#005A3C] text-white font-bold text-sm border-none cursor-pointer
                 hover:bg-[#007A52] transition-all disabled:opacity-50">
          <span v-if="changingStatut" class="loader"></span>
          {{ changingStatut ? 'Sauvegarde…' : '✅ Enregistrer' }}
        </button>
      </div>
    </div>
  </div>
</transition>

<!-- ════════════════════════════════════════════
     MODALE — Confirmation suppression
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="deleteModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.5)"
    @click.self="deleteModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center
                  text-3xl mx-auto mb-4">
        🗑️
      </div>
      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Supprimer cette déclaration ?
      </h3>

      <!-- Récap -->
      <div v-if="declToDelete"
        class="flex items-center gap-3 bg-gray-50 rounded-xl p-3 mb-3 text-left">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg"
          :style="{ backgroundColor: declToDelete.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
          {{ declToDelete.type_declaration === 'PERTE' ? '😟' : '🤲' }}
        </div>
        <div>
          <p class="font-mono text-sm font-bold text-[#005A3C]">
            {{ declToDelete.numero_recepisse }}
          </p>
          <p class="text-xs text-gray-400">{{ declToDelete.nom_sur_piece }}</p>
        </div>
      </div>

      <div class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-5 text-left">
        ⚠️ <strong>Action irréversible.</strong> La déclaration et ses notifications
        associées seront définitivement supprimées.
      </div>

      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        {{ apiError }}
      </div>

      <div class="flex gap-3">
        <button @click="deleteModal = false; apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDelete" :disabled="deleting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 hover:bg-[#e8192f] transition-all disabled:opacity-50">
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

.modal-enter-active, .modal-leave-active { transition: opacity .2s ease; }
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