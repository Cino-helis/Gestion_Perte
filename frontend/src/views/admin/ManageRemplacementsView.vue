<script setup>
/**
 * ManageRemplacementsView.vue
 * Interface agent/admin pour gérer les dossiers de remplacement.
 * Route : /admin/remplacements
 */
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminRemplacementsAPI } from '../../services/api'

const router = useRouter()

/* ══ État ══ */
const dossiers   = ref([])
const loading    = ref(true)
const apiError   = ref(null)
const apiSuccess = ref(null)
const search     = ref('')
const filterStatut = ref('')

/* ══ Modale de traitement ══ */
const modalOpen   = ref(false)
const selectedDossier = ref(null)
const submitting  = ref(false)
const form = ref({
  statut:               '',
  commissariat:         '',
  adresse_commissariat: '',
  horaires_commissariat:'',
  remarques:            '',
})
const formError = ref(null)

/* ══ Chargement ══ */
onMounted(loadDossiers)

async function loadDossiers() {
  loading.value  = true
  apiError.value = null
  try {
    const params = {}
    if (filterStatut.value) params.statut = filterStatut.value
    if (search.value)       params.search = search.value
    const { data } = await adminRemplacementsAPI.list(params)
    dossiers.value = data
  } catch (e) {
    apiError.value = 'Impossible de charger les dossiers.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage côté client ══ */
const filtered = computed(() => {
  let list = dossiers.value
  if (filterStatut.value) {
    list = list.filter(d => d.statut === filterStatut.value)
  }
  const q = search.value.toLowerCase().trim()
  if (q) {
    list = list.filter(d =>
      (d.numero_dossier || '').toLowerCase().includes(q) ||
      (d.declaration_recepisse || '').toLowerCase().includes(q) ||
      (d.declaration_nom || '').toLowerCase().includes(q) ||
      (d.declarant_nom || '').toLowerCase().includes(q) ||
      (d.declarant_username || '').toLowerCase().includes(q)
    )
  }
  return list
})

/* ══ Ouvrir la modale ══ */
function openModal(dossier) {
  selectedDossier.value = dossier
  form.value = {
    statut:                dossier.statut,
    commissariat:          dossier.commissariat || '',
    adresse_commissariat:  dossier.adresse_commissariat || '',
    horaires_commissariat: dossier.horaires_commissariat || '',
    remarques:             dossier.remarques || '',
  }
  formError.value  = null
  modalOpen.value  = true
}

/* ══ Soumettre le formulaire ══ */
async function handleSubmit() {
  if (!selectedDossier.value) return
  submitting.value = true
  formError.value  = null
  try {
    const { data } = await adminRemplacementsAPI.changerStatut(selectedDossier.value.id, form.value)
    // Mettre à jour la liste locale
    const idx = dossiers.value.findIndex(d => d.id === data.id)
    if (idx !== -1) dossiers.value[idx] = data
    apiSuccess.value = `✅ Dossier ${data.numero_dossier} mis à jour — ${getStatus(data.statut).label}`
    modalOpen.value  = false
    setTimeout(() => { apiSuccess.value = null }, 5000)
  } catch (e) {
    formError.value = e.response?.data?.error || JSON.stringify(e.response?.data) || 'Erreur lors de la mise à jour.'
  } finally {
    submitting.value = false
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE:     { label: 'En attente',          color: '#D97706', bg: '#FEF3C7', icon: '📂' },
  RECEPISSE_EMIS: { label: 'Autorisation émise',  color: '#2563EB', bg: '#DBEAFE', icon: '📄' },
  EN_TRAITEMENT:  { label: 'En traitement',        color: '#7C3AED', bg: '#EDE9FE', icon: '⚙️' },
  DOCUMENT_PRET:  { label: 'Pièce prête',         color: '#059669', bg: '#D1FAE5', icon: '🎉' },
  RETIRE:         { label: 'Retiré',              color: '#065F46', bg: '#A7F3D0', icon: '✅' },
  ANNULE:         { label: 'Annulé',              color: '#DC2626', bg: '#FEE2E2', icon: '❌' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

// Transitions autorisées selon le statut actuel
const transitionsAutorisees = computed(() => {
  if (!selectedDossier.value) return []
  const actuel = selectedDossier.value.statut
  const tout = Object.entries(statusConfig).map(([k, v]) => ({ value: k, label: `${v.icon} ${v.label}` }))
  const ordre = ['EN_ATTENTE', 'RECEPISSE_EMIS', 'EN_TRAITEMENT', 'DOCUMENT_PRET', 'RETIRE', 'ANNULE']
  const idx = ordre.indexOf(actuel)
  // Autoriser l'étape actuelle + les étapes suivantes + ANNULE
  return tout.filter(t => {
    const ti = ordre.indexOf(t.value)
    return ti >= idx || t.value === 'ANNULE'
  })
})

const stats = computed(() => ({
  total:         dossiers.value.length,
  en_attente:    dossiers.value.filter(d => d.statut === 'EN_ATTENTE').length,
  en_cours:      dossiers.value.filter(d => ['RECEPISSE_EMIS', 'EN_TRAITEMENT'].includes(d.statut)).length,
  pret:          dossiers.value.filter(d => d.statut === 'DOCUMENT_PRET').length,
  clotures:      dossiers.value.filter(d => d.statut === 'RETIRE').length,
}))

const statuts_filtre = Object.entries(statusConfig).map(([k, v]) => ({ value: k, label: `${v.icon} ${v.label}` }))
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-6xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-[#DBEAFE] text-[#2563EB]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🔄 Workflow de remplacement
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Dossiers de remplacement
      </h1>
      <p class="text-sm text-gray-500">
        Gérez les demandes de remplacement de pièces perdues (pertes sans match après 7 jours).
      </p>
    </div>
    <router-link :to="{ name: 'dashboard' }"
      class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
             bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
             hover:bg-gray-50 transition-all self-start">
      ← Tableau de bord
    </router-link>
  </div>

  <!-- ══ KPI Cards ══ -->
  <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 mb-6">
    <div v-for="c in [
      { label: 'Total',       val: stats.total,      icon: '📁', color: '#005A3C', bg: '#E8F4F0' },
      { label: 'En attente',  val: stats.en_attente, icon: '📂', color: '#D97706', bg: '#FEF3C7' },
      { label: 'En cours',    val: stats.en_cours,   icon: '⚙️', color: '#7C3AED', bg: '#EDE9FE' },
      { label: 'Pièce prête', val: stats.pret,       icon: '🎉', color: '#059669', bg: '#D1FAE5' },
      { label: 'Clôturés',   val: stats.clotures,   icon: '✅', color: '#065F46', bg: '#A7F3D0' },
    ]" :key="c.label"
      class="bg-white rounded-2xl border border-gray-100 shadow-card p-4 text-center">
      <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg mx-auto mb-1.5"
        :style="{ backgroundColor: c.bg }">{{ c.icon }}</div>
      <div class="font-serif text-xl font-bold" :style="{ color: c.color }">{{ c.val }}</div>
      <div class="text-xs text-gray-400 mt-0.5">{{ c.label }}</div>
    </div>
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
    <div v-if="apiError && !modalOpen"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Filtres ══ -->
  <div class="flex flex-wrap gap-3 mb-5">
    <div class="relative flex-1 min-w-[240px]">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="N° dossier, récépissé, nom du déclarant…"
        class="form-input pl-10 text-sm w-full"
        @input="loadDossiers"/>
    </div>
    <select v-model="filterStatut" class="form-input text-sm w-auto min-w-[200px]"
      @change="loadDossiers">
      <option value="">Tous les statuts</option>
      <option v-for="s in statuts_filtre" :key="s.value" :value="s.value">{{ s.label }}</option>
    </select>
    <button v-if="search || filterStatut"
      @click="search = ''; filterStatut = ''; loadDossiers()"
      class="text-xs text-gray-400 hover:text-rouge px-3 py-2 rounded-lg
             bg-white border border-gray-200 cursor-pointer transition-all hover:border-rouge/30">
      ✕ Réinitialiser
    </button>
  </div>

  <!-- ══ Résumé filtres ══ -->
  <p class="text-xs text-gray-500 mb-3">
    <span class="font-bold text-[#005A3C]">{{ filtered.length }}</span>
    dossier(s) affiché(s)
    <span v-if="filtered.length !== dossiers.length" class="text-gray-400">
      sur {{ dossiers.length }} au total
    </span>
  </p>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 5" :key="i" class="skeleton h-28 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">📂</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-1">Aucun dossier</p>
    <p class="text-sm text-gray-400">
      {{ search || filterStatut ? 'Aucun résultat pour ces filtres.' : 'Aucun dossier de remplacement pour l\'instant.' }}
    </p>
    <p class="text-xs text-gray-400 mt-2">
      Les dossiers sont créés automatiquement 7 jours après une perte sans correspondance.
    </p>
  </div>

  <!-- ══ Liste des dossiers ══ -->
  <div v-else class="space-y-3">
    <transition-group name="list-item">
      <div v-for="dossier in filtered" :key="dossier.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card transition-all hover:shadow-lg">

        <!-- Barre de progression -->
        <div class="h-1.5 rounded-t-2xl bg-gray-100 overflow-hidden">
          <div class="h-full rounded-t-2xl transition-all duration-700"
            :style="{
              width: `${dossier.progression_pct}%`,
              backgroundColor: getStatus(dossier.statut).color
            }">
          </div>
        </div>

        <div class="p-5 flex flex-col sm:flex-row items-start gap-4">

          <!-- Icône statut -->
          <div class="w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
            :style="{ backgroundColor: getStatus(dossier.statut).bg }">
            {{ getStatus(dossier.statut).icon }}
          </div>

          <!-- Infos -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-1">
              <span class="font-mono font-bold text-[#005A3C] text-sm tracking-wider">
                {{ dossier.numero_dossier }}
              </span>
              <span class="badge text-[10px] font-bold"
                :style="{ color: getStatus(dossier.statut).color, backgroundColor: getStatus(dossier.statut).bg }">
                {{ getStatus(dossier.statut).label }}
              </span>
              <span class="text-[10px] text-gray-400">{{ dossier.progression_pct }}%</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-0.5 text-xs text-gray-500 mb-2">
              <span>📋 Perte réf. : <strong class="font-mono">{{ dossier.declaration_recepisse }}</strong></span>
              <span>👤 {{ dossier.declarant_nom || dossier.declarant_username }}</span>
              <span>📁 {{ dossier.declaration_categorie }}</span>
              <span>📄 {{ dossier.declaration_nom }}</span>
            </div>

            <div class="flex items-center gap-4 text-[10px] text-gray-400 flex-wrap">
              <span>📅 Ouvert {{ formatDate(dossier.date_creation) }}</span>
              <span v-if="dossier.commissariat">🏛️ {{ dossier.commissariat }}</span>
              <span v-if="dossier.traite_par_nom">👮 {{ dossier.traite_par_nom }}</span>
              <span v-if="dossier.declarant_telephone">📞 {{ dossier.declarant_telephone }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0 sm:self-center">
            <button @click="openModal(dossier)"
              :disabled="['RETIRE', 'ANNULE'].includes(dossier.statut)"
              class="text-xs font-semibold text-white px-4 py-2.5 rounded-xl
                     border-none cursor-pointer transition-all hover:opacity-90
                     disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
              :style="{ backgroundColor: getStatus(dossier.statut).color }">
              ✏️ Traiter
            </button>
            <router-link
              :to="{ name: 'remplacement-detail', params: { id: dossier.id } }"
              class="text-xs font-semibold text-[#005A3C] bg-[#E8F4F0] hover:bg-[#c8e8dc]
                     px-3 py-2.5 rounded-xl no-underline transition-all">
              👁️ Voir
            </router-link>
          </div>
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════════════
     MODALE — Traiter un dossier
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="modalOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto"
    style="background:rgba(0,0,0,.5)"
    @click.self="modalOpen = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl my-4">

      <!-- En-tête modale -->
      <div class="flex items-center justify-between p-6 border-b border-gray-100">
        <div>
          <h2 class="font-serif text-lg font-bold text-[#1A2E22]">
            Traiter le dossier
          </h2>
          <p class="text-xs text-gray-500 mt-0.5 font-mono">
            {{ selectedDossier?.numero_dossier }}
            — {{ selectedDossier?.declarant_nom }}
          </p>
        </div>
        <button @click="modalOpen = false"
          class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center
                 text-gray-500 border-none cursor-pointer hover:bg-gray-200 transition-all">
          ✕
        </button>
      </div>

      <div class="p-6 space-y-5">

        <!-- Erreur formulaire -->
        <div v-if="formError"
          class="flex items-center gap-2 bg-red-50 border border-red-200
                 rounded-xl p-3 text-sm text-rouge">
          ⚠️ {{ formError }}
        </div>

        <!-- Récapitulatif déclarant -->
        <div class="bg-gray-50 rounded-xl p-4 text-sm space-y-1">
          <div class="flex gap-4 flex-wrap text-xs text-gray-500">
            <span>👤 <strong>{{ selectedDossier?.declarant_nom }}</strong></span>
            <span v-if="selectedDossier?.declarant_telephone">📞 {{ selectedDossier?.declarant_telephone }}</span>
            <span v-if="selectedDossier?.declarant_email">✉️ {{ selectedDossier?.declarant_email }}</span>
          </div>
          <div class="flex gap-4 flex-wrap text-xs text-gray-500 mt-1">
            <span>📋 {{ selectedDossier?.declaration_recepisse }}</span>
            <span>📁 {{ selectedDossier?.declaration_categorie }}</span>
            <span>📄 {{ selectedDossier?.declaration_nom }}</span>
          </div>
        </div>

        <!-- Nouveau statut -->
        <div>
          <label class="form-label">Nouveau statut <span class="text-rouge">*</span></label>
          <div class="grid grid-cols-1 gap-2">
            <button v-for="t in transitionsAutorisees" :key="t.value"
              type="button"
              @click="form.statut = t.value"
              :class="[
                'flex items-center gap-3 p-3 rounded-xl border-2 text-left transition-all cursor-pointer',
                form.statut === t.value
                  ? 'border-[#005A3C] bg-[#E8F4F0]'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              ]">
              <span class="text-base">{{ getStatus(t.value).icon }}</span>
              <span class="text-sm font-semibold text-[#1A2E22]">{{ getStatus(t.value).label }}</span>
              <span v-if="form.statut === t.value"
                class="ml-auto w-5 h-5 bg-[#005A3C] rounded-full flex items-center justify-center text-white text-xs">✓</span>
            </button>
          </div>
        </div>

        <!-- Commissariat (affiché si statut = RECEPISSE_EMIS ou EN_TRAITEMENT) -->
        <template v-if="['RECEPISSE_EMIS', 'EN_TRAITEMENT', 'DOCUMENT_PRET'].includes(form.statut)">
          <div>
            <label class="form-label">
              Commissariat agréé
              <span v-if="form.statut === 'RECEPISSE_EMIS'" class="text-rouge">*</span>
              <span v-else class="text-gray-400 normal-case font-normal">(optionnel)</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🏛️</span>
              <input v-model="form.commissariat" type="text"
                placeholder="Ex : Commissariat Central de Lomé"
                class="form-input pl-10"/>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="form-label">Adresse <span class="text-gray-400 normal-case font-normal">(opt.)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">📍</span>
                <input v-model="form.adresse_commissariat" type="text"
                  placeholder="Avenue de la Paix, Lomé"
                  class="form-input pl-10"/>
              </div>
            </div>
            <div>
              <label class="form-label">Horaires <span class="text-gray-400 normal-case font-normal">(opt.)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🕐</span>
                <input v-model="form.horaires_commissariat" type="text"
                  placeholder="Lun.–Ven. 08h–16h"
                  class="form-input pl-10"/>
              </div>
            </div>
          </div>
        </template>

        <!-- Remarques -->
        <div>
          <label class="form-label">
            Remarques <span class="text-gray-400 normal-case font-normal">(optionnel)</span>
          </label>
          <textarea v-model="form.remarques" rows="3"
            placeholder="Message pour le citoyen, instructions particulières…"
            class="form-input resize-none text-sm">
          </textarea>
        </div>

        <!-- Info : email et notification automatiques -->
        <div class="bg-[#E8F4F0] border border-[#005A3C]/20 rounded-xl p-3 text-xs text-[#005A3C]">
          📧 <strong>Automatique :</strong> Le citoyen recevra une notification in-app
          et un email Gmail à chaque changement de statut.
        </div>

      </div>

      <!-- Pied de modale -->
      <div class="flex gap-3 p-6 border-t border-gray-100">
        <button type="button" @click="modalOpen = false"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 transition-all cursor-pointer">
          Annuler
        </button>
        <button type="button" @click="handleSubmit"
          :disabled="submitting || !form.statut"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-[#005A3C] text-white font-bold text-sm border-none cursor-pointer
                 hover:bg-[#007A52] transition-all disabled:opacity-50">
          <span v-if="submitting" class="loader"></span>
          {{ submitting ? 'Enregistrement…' : '✅ Enregistrer' }}
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
.list-item-leave-active { transition: all .2s ease; position: absolute; width: 100%; }
.list-item-leave-to     { opacity: 0; transform: translateX(20px); }

.modal-enter-active, .modal-leave-active { transition: opacity .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: transform .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-6px); }

.loader {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
