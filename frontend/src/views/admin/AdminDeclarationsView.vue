<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declarations  = ref([])
const loading       = ref(true)
const apiError      = ref(null)
const search        = ref('')
const filterType    = ref('ALL')
const filterStatut  = ref('ALL')
const modalOpen     = ref(false)
const selectedDecl  = ref(null)
const newStatut     = ref('')
const remarques     = ref('')
const saving        = ref(false)
const saveSuccess   = ref(null)

/* ══ Chargement ══ */
onMounted(async () => {
  await loadDeclarations()
})

const loadDeclarations = async () => {
  loading.value = true
  try {
    const { data } = await declarationsAPI.list()
    declarations.value = data.results ?? data
  } catch {
    apiError.value = 'Impossible de charger les déclarations.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage + recherche ══ */
const filtered = computed(() => {
  let list = declarations.value
  const q  = search.value.toLowerCase().trim()

  if (q) list = list.filter(d =>
    d.numero_piece.toLowerCase().includes(q) ||
    d.nom_sur_piece.toLowerCase().includes(q) ||
    (d.numero_recepisse || '').toLowerCase().includes(q) ||
    (d.declarant || '').toLowerCase().includes(q)
  )
  if (filterType.value !== 'ALL')
    list = list.filter(d => d.type_declaration === filterType.value)
  if (filterStatut.value !== 'ALL')
    list = list.filter(d => d.statut === filterStatut.value)

  return list
})

/* ══ Modal changement de statut ══ */
const openModal = (decl) => {
  selectedDecl.value = decl
  newStatut.value    = decl.statut
  remarques.value    = ''
  saveSuccess.value  = null
  apiError.value     = null
  modalOpen.value    = true
}
const closeModal = () => {
  modalOpen.value   = false
  selectedDecl.value = null
}

const applyStatut = async () => {
  if (!selectedDecl.value || !newStatut.value) return
  saving.value = true
  try {
    const { data } = await declarationsAPI.changerStatut(selectedDecl.value.id, {
      statut:   newStatut.value,
      remarques: remarques.value,
    })
    // Mettre à jour dans la liste locale
    const idx = declarations.value.findIndex(d => d.id === data.id)
    if (idx !== -1) {
      declarations.value[idx] = {
        ...declarations.value[idx],
        statut: data.statut,
      }
    }
    selectedDecl.value.statut = data.statut
    saveSuccess.value = 'Statut mis à jour avec succès !'
    setTimeout(closeModal, 1200)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la mise à jour.'
  } finally {
    saving.value = false
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente',  color: '#D97706', bg: '#FEF3C7', icon: '⏳' },
  VALIDE:     { label: 'Validé',      color: '#2563EB', bg: '#DBEAFE', icon: '✅' },
  RETROUVE:   { label: 'Retrouvé',    color: '#059669', bg: '#D1FAE5', icon: '🎉' },
  RESTITUE:   { label: 'Restitué',    color: '#065F46', bg: '#A7F3D0', icon: '🤝' },
  REJETE:     { label: 'Rejeté',      color: '#DC2626', bg: '#FEE2E2', icon: '❌' },
  CLOTURE:    { label: 'Clôturé',     color: '#6B7280', bg: '#F3F4F6', icon: '🔒' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const statuts = Object.entries(statusConfig).map(([k, v]) => ({ key: k, ...v }))

const downloadPDF = async (decl) => {
  try {
    const { data } = await declarationsAPI.downloadPDF(decl.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${decl.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch {}
}
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-6xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full mb-3"
        :style="{ backgroundColor: authStore.isAdmin ? '#FEE2E2' : '#DBEAFE',
                  color: authStore.isAdmin ? '#C41230' : '#2563EB' }">
        {{ authStore.isAdmin ? '🛡️ Administration' : '👮 Police' }}
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des déclarations
      </h1>
      <p class="text-sm text-gray-500">
        {{ filtered.length }} déclaration{{ filtered.length !== 1 ? 's' : '' }} affichée{{ filtered.length !== 1 ? 's' : '' }}
        sur {{ declarations.length }} au total
      </p>
    </div>
    <router-link :to="{ name: 'dashboard' }"
      class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
             bg-white border border-gray-200 px-5 py-3 rounded-xl no-underline
             hover:bg-gray-50 transition-all">
      ← Tableau de bord
    </router-link>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="apiError && !modalOpen"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-5 text-sm text-rouge">
    <span>⚠️</span><span>{{ apiError }}</span>
    <button @click="apiError = null" class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
  </div>

  <!-- ══ Barre de filtres ══ -->
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-4 mb-5
              flex flex-col sm:flex-row items-start sm:items-center gap-3 flex-wrap">

    <!-- Recherche -->
    <div class="relative flex-1 min-w-[200px]">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher par numéro, nom, récépissé…"
        class="form-input pl-9 text-sm"/>
    </div>

    <!-- Type -->
    <div class="flex items-center gap-1 bg-gray-50 rounded-xl p-1 border border-gray-200">
      <button v-for="opt in [
        { key: 'ALL',        label: 'Tous' },
        { key: 'PERTE',      label: '😟 Pertes' },
        { key: 'TROUVAILLE', label: '🤲 Trouvailles' },
      ]" :key="opt.key"
        @click="filterType = opt.key"
        :class="[
          'text-xs font-semibold px-3 py-1.5 rounded-lg transition-all cursor-pointer border-none',
          filterType === opt.key
            ? 'bg-[#005A3C] text-white shadow-sm'
            : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
        ]">
        {{ opt.label }}
      </button>
    </div>

    <!-- Statut -->
    <select v-model="filterStatut"
      class="bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 text-xs
             text-gray-600 outline-none cursor-pointer">
      <option value="ALL">Tous statuts</option>
      <option v-for="s in statuts" :key="s.key" :value="s.key">
        {{ s.icon }} {{ s.label }}
      </option>
    </select>

    <!-- Reset -->
    <button v-if="search || filterType !== 'ALL' || filterStatut !== 'ALL'"
      @click="search = ''; filterType = 'ALL'; filterStatut = 'ALL'"
      class="text-xs text-rouge bg-transparent border-none cursor-pointer hover:underline">
      ✕ Réinitialiser
    </button>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Tableau ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl shadow-card border border-gray-100">
    <div class="text-4xl mb-3">🗂️</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-2">Aucune déclaration</p>
    <p class="text-sm text-gray-500">Aucun résultat pour ces filtres.</p>
  </div>

  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="decl in filtered" :key="decl.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card
               hover:shadow-card-lg transition-all">
        <div class="p-4 flex flex-col sm:flex-row items-start gap-4">

          <!-- Icône -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
            :style="{ backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>

          <!-- Infos principales -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2 flex-wrap">
              <div>
                <span class="font-mono font-bold text-[#005A3C] text-sm tracking-wider">
                  {{ decl.numero_piece }}
                </span>
                <span class="mx-2 text-gray-300">·</span>
                <span class="text-sm font-semibold text-[#1A2E22]">
                  {{ decl.nom_sur_piece }}
                </span>
              </div>
              <span class="badge text-xs flex-shrink-0"
                :style="{
                  color: getStatus(decl.statut).color,
                  backgroundColor: getStatus(decl.statut).bg
                }">
                {{ getStatus(decl.statut).icon }} {{ getStatus(decl.statut).label }}
              </span>
            </div>

            <div class="flex items-center gap-3 text-xs text-gray-400 flex-wrap mt-1.5">
              <span>👤 {{ decl.declarant }}</span>
              <span>📅 {{ formatDate(decl.date_declaration) }}</span>
              <span v-if="decl.categorie_nom">📁 {{ decl.categorie_nom }}</span>
              <span class="font-mono text-[10px] text-gray-300">{{ decl.numero_recepisse }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0 sm:self-center">
            <!-- Voir -->
            <button @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
              class="text-xs font-medium text-gray-500 bg-gray-100 hover:bg-gray-200
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              👁️
            </button>
            <!-- PDF -->
            <button @click="downloadPDF(decl)"
              class="text-xs font-medium text-[#005A3C] bg-[#E8F4F0] hover:bg-[#d0ece3]
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              📄
            </button>
            <!-- Changer statut -->
            <button @click="openModal(decl)"
              class="text-xs font-bold text-white bg-[#005A3C] hover:bg-[#007A52]
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              ✏️ Statut
            </button>
          </div>

        </div>
        <!-- Barre statut -->
        <div class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getStatus(decl.statut).color, opacity: 0.3 }">
        </div>
      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════
     MODAL — Changer le statut
════════════════════════════════════ -->
<transition name="modal">
  <div v-if="modalOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background: rgba(0,0,0,.45);"
    @click.self="closeModal">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 relative">

      <!-- Fermer -->
      <button @click="closeModal"
        class="absolute top-4 right-4 w-8 h-8 rounded-full bg-gray-100
               flex items-center justify-center text-gray-500 text-sm
               hover:bg-gray-200 border-none cursor-pointer transition-all">
        ✕
      </button>

      <h2 class="font-serif text-xl font-bold text-[#1A2E22] mb-1">
        Changer le statut
      </h2>
      <p class="text-xs text-gray-500 mb-5">
        Déclaration <span class="font-mono font-bold text-[#005A3C]">{{ selectedDecl?.numero_recepisse }}</span>
        — {{ selectedDecl?.nom_sur_piece }}
      </p>

      <!-- Succès inline -->
      <div v-if="saveSuccess"
        class="flex items-center gap-2 bg-green-50 border border-green-200
               rounded-xl p-3 mb-4 text-sm text-green-700">
        <span>✅</span><span>{{ saveSuccess }}</span>
      </div>

      <!-- Erreur inline -->
      <div v-if="apiError"
        class="flex items-center gap-2 bg-red-50 border border-red-200
               rounded-xl p-3 mb-4 text-sm text-rouge">
        <span>⚠️</span><span>{{ apiError }}</span>
      </div>

      <!-- Sélecteur statut -->
      <div class="mb-4">
        <label class="form-label">Nouveau statut</label>
        <div class="grid grid-cols-2 gap-2">
          <button v-for="s in statuts" :key="s.key"
            type="button"
            @click="newStatut = s.key"
            :class="[
              'flex items-center gap-2 px-3 py-2.5 rounded-xl border-2 text-xs font-semibold',
              'transition-all cursor-pointer text-left',
              newStatut === s.key
                ? 'border-[#005A3C] shadow-sm'
                : 'border-gray-200 bg-white hover:border-gray-300'
            ]"
            :style="newStatut === s.key
              ? { backgroundColor: s.bg, color: s.color }
              : {}">
            <span>{{ s.icon }}</span>
            <span>{{ s.label }}</span>
          </button>
        </div>
      </div>

      <!-- Remarques -->
      <div class="mb-5">
        <label class="form-label">
          Remarques <span class="text-gray-400 normal-case font-normal">(optionnel)</span>
        </label>
        <textarea v-model="remarques" rows="3"
          placeholder="Ajoutez une note visible par le déclarant…"
          class="form-input resize-none text-sm"></textarea>
      </div>

      <!-- Boutons -->
      <div class="flex gap-3">
        <button @click="closeModal"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 transition-all cursor-pointer">
          Annuler
        </button>
        <button @click="applyStatut"
          :disabled="saving || !newStatut || newStatut === selectedDecl?.statut"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-[#005A3C] text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="saving" class="loader-dot"></span>
          <span v-else>✅</span>
          {{ saving ? 'Enregistrement…' : 'Confirmer' }}
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

.loader-dot {
  display: inline-block; width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>