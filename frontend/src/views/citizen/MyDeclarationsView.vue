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
const filterType   = ref('ALL')    // ALL | PERTE | TROUVAILLE
const filterStatut = ref('ALL')
const downloading  = ref(null)     // id en cours de download

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await declarationsAPI.myDeclarations()
    declarations.value = data.results ?? data
  } catch (e) {
    apiError.value = 'Impossible de charger vos déclarations.'
  } finally {
    loading.value = false
  }
})

/* ══ Filtrage ══ */
const filtered = computed(() => {
  let list = declarations.value
  if (filterType.value !== 'ALL')
    list = list.filter(d => d.type_declaration === filterType.value)
  if (filterStatut.value !== 'ALL')
    list = list.filter(d => d.statut === filterStatut.value)
  return list
})

/* ══ Statistiques ══ */
const stats = computed(() => {
  const d = declarations.value
  return {
    total:     d.length,
    pertes:    d.filter(x => x.type_declaration === 'PERTE').length,
    attente:   d.filter(x => x.statut === 'EN_ATTENTE').length,
    retrouve:  d.filter(x => x.statut === 'RETROUVE').length,
    restitue:  d.filter(x => x.statut === 'RESTITUE').length,
  }
})

/* ══ Téléchargement PDF ══ */
const downloadPDF = async (decl) => {
  downloading.value = decl.id
  try {
    const { data } = await declarationsAPI.downloadPDF(decl.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${decl.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    apiError.value = 'Erreur lors de la génération du PDF.'
  } finally {
    downloading.value = null
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
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-4xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-8 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        👤 Espace citoyen
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Bonjour, {{ authStore.user?.first_name || authStore.user?.username }} 👋
      </h1>
      <p class="text-sm text-gray-500">
        Suivez l'état de vos déclarations et téléchargez vos récépissés.
      </p>
    </div>
    <router-link :to="{ name: 'declare' }"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-5 py-3 rounded-xl no-underline hover:bg-[#007A52]
             hover:-translate-y-0.5 transition-all shadow-md flex-shrink-0">
      + Nouvelle déclaration
    </router-link>
  </div>

  <!-- ══ Statistiques ══ -->
  <div v-if="!loading" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-[#005A3C]">{{ stats.total }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Total</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-yellow-600">{{ stats.attente }}</div>
      <div class="text-xs text-gray-500 mt-0.5">En attente</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-green-600">{{ stats.retrouve }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Retrouvées</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-emerald-700">{{ stats.restitue }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Restituées</div>
    </div>
  </div>

  <!-- Squelettes stats -->
  <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
    <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-xl"></div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="apiError"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-6 text-sm text-rouge">
    <span>⚠️</span><span>{{ apiError }}</span>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex items-center gap-2 mb-5 flex-wrap">
    <!-- Type -->
    <div class="flex items-center gap-1 bg-white rounded-xl p-1 border border-gray-200 shadow-sm">
      <button v-for="opt in [
        { key: 'ALL',       label: 'Tous'        },
        { key: 'PERTE',     label: '😟 Pertes'   },
        { key: 'TROUVAILLE',label: '🤲 Trouvailles'},
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
      class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs
             text-gray-600 outline-none cursor-pointer shadow-sm">
      <option value="ALL">Tous les statuts</option>
      <option v-for="s in statuts" :key="s.key" :value="s.key">
        {{ s.icon }} {{ s.label }}
      </option>
    </select>

    <span class="ml-auto text-xs text-gray-400">
      {{ filtered.length }} résultat{{ filtered.length !== 1 ? 's' : '' }}
    </span>
  </div>

  <!-- ══ Liste squelette ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 4" :key="i" class="skeleton h-28 rounded-2xl"></div>
  </div>

  <!-- ══ Liste vide ══ -->
  <div v-else-if="filtered.length === 0 && declarations.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-5xl mb-4">📂</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">Aucune déclaration</p>
    <p class="text-sm text-gray-500 mb-6">
      Vous n'avez pas encore fait de déclaration.
    </p>
    <router-link :to="{ name: 'declare' }"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-6 py-3 rounded-xl no-underline hover:bg-[#007A52] transition-all">
      📋 Faire ma première déclaration
    </router-link>
  </div>

  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500">Aucune déclaration ne correspond aux filtres.</p>
    <button @click="filterType = 'ALL'; filterStatut = 'ALL'"
      class="mt-3 text-xs text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      Réinitialiser les filtres
    </button>
  </div>

  <!-- ══ Cartes déclarations ══ -->
  <div v-else class="space-y-3">
    <transition-group name="list-item">
      <div v-for="decl in filtered" :key="decl.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card
               hover:shadow-card-lg hover:-translate-y-0.5 transition-all">

        <div class="p-5 flex flex-col sm:flex-row items-start gap-4">

          <!-- Icône type -->
          <div class="w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
            :style="{
              backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
            }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>

          <!-- Contenu principal -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2 flex-wrap mb-1.5">
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

            <div class="flex items-center gap-3 text-xs text-gray-400 flex-wrap">
              <span>📅 {{ formatDate(decl.date_declaration) }}</span>
              <span v-if="decl.categorie_nom">📁 {{ decl.categorie_nom }}</span>
              <span v-if="decl.lieu_perte">📍 {{ decl.lieu_perte }}</span>
              <span class="font-mono text-[10px] text-gray-300">{{ decl.numero_recepisse }}</span>
            </div>

            <!-- Alerte match -->
            <div v-if="decl.statut === 'RETROUVE'"
              class="mt-2 inline-flex items-center gap-1.5 bg-green-50 text-green-700
                     text-xs font-semibold px-3 py-1.5 rounded-lg">
              🎉 Correspondance trouvée — Voir les détails
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0 sm:self-center">
            <!-- Télécharger PDF -->
            <button @click="downloadPDF(decl)"
              :disabled="downloading === decl.id"
              class="flex items-center gap-1.5 text-xs font-semibold
                     text-[#005A3C] bg-[#E8F4F0] hover:bg-[#d0ece3]
                     px-3 py-2 rounded-lg border-none cursor-pointer
                     transition-all disabled:opacity-50 disabled:cursor-wait">
              <span v-if="downloading === decl.id" class="loader-dot-xs"></span>
              <span v-else>📄</span>
              PDF
            </button>
            <!-- Voir détail -->
            <button @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
              class="flex items-center gap-1.5 text-xs font-semibold
                     text-gray-600 bg-gray-100 hover:bg-gray-200
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              Détails →
            </button>
          </div>

        </div>

        <!-- Barre de statut en bas de carte (couleur) -->
        <div class="h-0.5 rounded-b-2xl transition-all"
          :style="{ backgroundColor: getStatus(decl.statut).color, opacity: 0.4 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>
</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(10px); }

.loader-dot-xs {
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid rgba(0,90,60,.2);
  border-top-color: #005A3C;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>