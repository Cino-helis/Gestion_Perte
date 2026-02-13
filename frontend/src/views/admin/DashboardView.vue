<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { statsAPI, declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const stats   = ref(null)
const loading = ref(true)
const error   = ref(null)

/* ══ Chargement des stats ══ */
onMounted(async () => {
  try {
    const { data } = await statsAPI.get()
    stats.value = data
    // Charger Chart.js uniquement si disponible
    await renderCharts()
  } catch (e) {
    error.value = 'Impossible de charger les statistiques.'
  } finally {
    loading.value = false
  }
})

/* ══ Graphiques (Chart.js via CDN) ══ */
const chartLoaded = ref(false)

const renderCharts = async () => {
  // Chart.js est chargé via CDN dans index.html ou importé ici
  if (typeof window === 'undefined') return
  try {
    const { Chart, registerables } = await import('https://cdn.jsdelivr.net/npm/chart.js@4/+esm')
    Chart.register(...registerables)
    chartLoaded.value = true

    // Petit délai pour que les canvas soient dans le DOM
    await new Promise(r => setTimeout(r, 100))

    const s = stats.value
    if (!s) return

    // Graphique en anneau — Répartition par type
    const donutCtx = document.getElementById('donutChart')
    if (donutCtx) {
      new Chart(donutCtx, {
        type: 'doughnut',
        data: {
          labels: ['Pertes', 'Trouvailles'],
          datasets: [{
            data: [s.total_pertes, s.total_trouvailles],
            backgroundColor: ['#C41230', '#005A3C'],
            borderWidth: 0,
            hoverOffset: 6,
          }]
        },
        options: {
          responsive: true,
          cutout: '72%',
          plugins: {
            legend: {
              position: 'bottom',
              labels: { boxWidth: 10, padding: 14, font: { size: 11 } }
            }
          }
        }
      })
    }

    // Graphique en barres — Répartition par statut
    const barCtx = document.getElementById('barChart')
    if (barCtx) {
      new Chart(barCtx, {
        type: 'bar',
        data: {
          labels: ['En attente', 'Validées', 'Retrouvées', 'Restituées'],
          datasets: [{
            data: [s.en_attente, s.validees, s.retrouvees, s.restituees],
            backgroundColor: ['#FEF3C7', '#DBEAFE', '#D1FAE5', '#A7F3D0'],
            borderColor:     ['#D97706',  '#2563EB', '#059669', '#065F46'],
            borderWidth: 2,
            borderRadius: 8,
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: '#f3f4f6' }, ticks: { stepSize: 1 } },
            x: { grid: { display: false } }
          }
        }
      })
    }

  } catch (e) {
    // Chart.js indisponible — mode dégradé sans graphiques
    console.warn('Chart.js non disponible:', e)
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente',  color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',      color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',    color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',    color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',      color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',     color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const taux = computed(() => {
  if (!stats.value || !stats.value.total_declarations) return 0
  return Math.round(
    ((stats.value.retrouvees + stats.value.restituees) / stats.value.total_declarations) * 100
  )
})

const kpiCards = computed(() => {
  if (!stats.value) return []
  const s = stats.value
  return [
    { label: 'Total déclarations', value: s.total_declarations, icon: '📋', color: '#005A3C', bg: '#E8F4F0', sub: `${s.total_pertes} pertes · ${s.total_trouvailles} trouvailles` },
    { label: 'En attente',         value: s.en_attente,         icon: '⏳', color: '#D97706', bg: '#FEF3C7', sub: 'À valider' },
    { label: 'Retrouvées',         value: s.retrouvees,         icon: '🎉', color: '#059669', bg: '#D1FAE5', sub: `Taux : ${taux.value}%` },
    { label: 'Restituées',         value: s.restituees,         icon: '🤝', color: '#065F46', bg: '#A7F3D0', sub: 'Clôturées avec succès' },
  ]
})
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-5xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-8 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full mb-3"
        :style="{ backgroundColor: authStore.isAdmin ? '#FEE2E2' : '#DBEAFE',
                  color: authStore.isAdmin ? '#C41230' : '#2563EB' }">
        {{ authStore.isAdmin ? '🛡️ Administrateur' : '👮 Agent de Police' }}
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Tableau de bord
      </h1>
      <p class="text-sm text-gray-500">Vue d'ensemble de la plateforme DéclaTogo.</p>
    </div>
    <router-link :to="{ name: 'admin-declarations' }"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-5 py-3 rounded-xl no-underline hover:bg-[#007A52]
             hover:-translate-y-0.5 transition-all shadow-md">
      📋 Gérer les déclarations
    </router-link>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="error"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-6 text-sm text-rouge">
    <span>⚠️</span><span>{{ error }}</span>
  </div>

  <!-- ══ KPI Cards ══ -->
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <template v-if="loading">
      <div v-for="i in 4" :key="i" class="skeleton h-28 rounded-2xl"></div>
    </template>
    <template v-else>
      <div v-for="card in kpiCards" :key="card.label"
        class="bg-white rounded-2xl shadow-card border border-gray-100 p-5
               hover:-translate-y-0.5 hover:shadow-card-lg transition-all">
        <div class="flex items-start justify-between mb-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
            :style="{ backgroundColor: card.bg }">
            {{ card.icon }}
          </div>
          <div class="font-serif text-3xl font-bold leading-none"
            :style="{ color: card.color }">
            {{ card.value }}
          </div>
        </div>
        <div class="text-xs font-semibold text-[#1A2E22]">{{ card.label }}</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ card.sub }}</div>
      </div>
    </template>
  </div>

  <!-- ══ Graphiques + Catégories ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">

    <!-- Anneau -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">
        Répartition par type
      </h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <div v-else class="relative flex items-center justify-center">
        <canvas id="donutChart" height="180"></canvas>
        <!-- Valeur centrale -->
        <div v-if="!chartLoaded" class="text-center">
          <div class="font-serif text-3xl font-bold text-[#005A3C]">{{ stats?.total_declarations || 0 }}</div>
          <div class="text-xs text-gray-400">Total</div>
        </div>
      </div>
    </div>

    <!-- Barres statuts -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 lg:col-span-2">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">
        Répartition par statut
      </h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <canvas v-else id="barChart" height="140"></canvas>
    </div>

  </div>

  <!-- ══ Catégories populaires + Déclarations récentes ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

    <!-- Catégories populaires -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4 flex items-center gap-2">
        <span class="w-6 h-6 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-xs">📁</span>
        Catégories actives
      </h2>
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 5" :key="i" class="skeleton h-8 rounded-lg"></div>
      </div>
      <div v-else-if="stats?.categories_populaires?.length" class="space-y-2">
        <div v-for="(cat, i) in stats.categories_populaires" :key="cat.libelle"
          class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <span class="text-xs font-bold text-[#005A3C] w-4 flex-shrink-0">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-[#1A2E22] truncate">{{ cat.libelle }}</div>
              <div class="h-1 bg-gray-100 rounded-full mt-1 overflow-hidden">
                <div class="h-full bg-[#005A3C] rounded-full transition-all"
                  :style="{ width: `${Math.min(100, (cat.nombre / (stats.total_declarations || 1)) * 100)}%` }">
                </div>
              </div>
            </div>
          </div>
          <span class="text-xs font-bold text-gray-500 flex-shrink-0">{{ cat.nombre }}</span>
        </div>
      </div>
      <p v-else class="text-xs text-gray-400">Aucune donnée disponible.</p>
    </div>

    <!-- Déclarations récentes -->
    <div class="lg:col-span-2 bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-serif text-sm font-bold text-[#1A2E22] flex items-center gap-2">
          <span class="w-6 h-6 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-xs">🕐</span>
          Déclarations récentes
        </h2>
        <router-link :to="{ name: 'admin-declarations' }"
          class="text-xs text-[#005A3C] font-semibold no-underline hover:underline">
          Voir tout →
        </router-link>
      </div>

      <div v-if="loading" class="space-y-3">
        <div v-for="i in 4" :key="i" class="skeleton h-14 rounded-xl"></div>
      </div>

      <div v-else-if="stats?.declarations_recentes?.length" class="space-y-2">
        <div v-for="decl in stats.declarations_recentes.slice(0, 6)" :key="decl.id"
          @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
          class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50
                 transition-all cursor-pointer">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
            :style="{ backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold text-[#005A3C] tracking-wide truncate">
                {{ decl.numero_piece }}
              </span>
              <span class="badge text-[10px] flex-shrink-0"
                :style="{
                  color: getStatus(decl.statut).color,
                  backgroundColor: getStatus(decl.statut).bg
                }">
                {{ getStatus(decl.statut).label }}
              </span>
            </div>
            <div class="flex items-center gap-2 text-[10px] text-gray-400 mt-0.5">
              <span>{{ decl.nom_sur_piece }}</span>
              <span>·</span>
              <span>{{ formatDate(decl.date_declaration) }}</span>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="text-xs text-gray-400 py-4 text-center">Aucune déclaration récente.</p>

    </div>
  </div>

</div>
</div>
</template>