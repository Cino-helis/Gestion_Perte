<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { statsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

const stats   = ref(null)
const loading = ref(true)
const error   = ref(null)

onMounted(async () => {
  try {
    const { data } = await statsAPI.get()
    stats.value = data
    await renderCharts()
  } catch (e) {
    error.value = 'Impossible de charger les statistiques.'
  } finally {
    loading.value = false
  }
})

const chartLoaded = ref(false)

const renderCharts = async () => {
  if (typeof window === 'undefined') return
  try {
    const { Chart, registerables } = await import('https://cdn.jsdelivr.net/npm/chart.js@4/+esm')
    Chart.register(...registerables)
    chartLoaded.value = true
    await new Promise(r => setTimeout(r, 100))
    const s = stats.value
    if (!s) return

    const donutCtx = document.getElementById('donutChart')
    if (donutCtx) {
      new Chart(donutCtx, {
        type: 'doughnut',
        data: {
          labels: ['Pertes', 'Trouvailles'],
          datasets: [{
            data: [s.total_pertes, s.total_trouvailles],
            backgroundColor: ['#C41230', '#005A3C'],
            borderWidth: 0, hoverOffset: 6,
          }]
        },
        options: {
          responsive: true, cutout: '72%',
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 10, padding: 14, font: { size: 11 } } }
          }
        }
      })
    }

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
            borderWidth: 2, borderRadius: 8,
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
  } catch (e) { console.warn('Chart.js:', e) }
}

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

const taux = computed(() => {
  if (!stats.value?.total_declarations) return 0
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
    { label: 'Utilisateurs',       value: s.total_utilisateurs || '—', icon: '👥', color: '#2563EB', bg: '#DBEAFE', sub: `${s.total_citoyens || 0} citoyens · ${s.total_agents || 0} agents` },
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
        :style="{
          backgroundColor: authStore.isAdmin ? '#FEE2E2' : '#DBEAFE',
          color: authStore.isAdmin ? '#C41230' : '#2563EB'
        }">
        {{ authStore.isAdmin ? '🛡️ Administrateur' : '👮 Agent de Police' }}
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">Tableau de bord</h1>
      <p class="text-sm text-gray-500">Vue d'ensemble de la plateforme DéclaTogo.</p>
    </div>

    <!-- Actions rapides ─────────────────────────── -->
    <div class="flex items-center gap-2 flex-wrap">
      <router-link v-if="authStore.isAdmin"
        :to="{ name: 'admin-users' }"
        class="inline-flex items-center gap-2 text-sm font-bold px-4 py-3 rounded-xl
               no-underline transition-all hover:-translate-y-0.5 shadow"
        style="background-color:#2563EB; color:white;">
        👥 Utilisateurs
      </router-link>
      <router-link v-if="authStore.isAdmin"
        :to="{ name: 'admin-agents' }"
        class="inline-flex items-center gap-2 text-sm font-bold px-4 py-3 rounded-xl
               no-underline transition-all hover:-translate-y-0.5 shadow"
        style="background-color:#C41230; color:white;">
        👮 Agents
      </router-link>
      <router-link :to="{ name: 'admin-declarations' }"
        class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
               text-sm px-4 py-3 rounded-xl no-underline hover:bg-[#007A52]
               hover:-translate-y-0.5 transition-all shadow">
        📋 Déclarations
      </router-link>
    </div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="error"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-6 text-sm text-rouge">
    ⚠️ {{ error }}
  </div>

  <!-- ══ KPI Cards ══ -->
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <div v-if="loading" v-for="i in 4" :key="i" class="skeleton h-28 rounded-2xl"></div>
    <template v-else>
      <div v-for="card in kpiCards" :key="card.label"
        class="bg-white rounded-2xl shadow-card border border-gray-100 p-5
               hover:-translate-y-0.5 hover:shadow-card-lg transition-all">
        <div class="flex items-start justify-between mb-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
            :style="{ backgroundColor: card.bg }">{{ card.icon }}</div>
          <div class="font-serif text-3xl font-bold" :style="{ color: card.color }">
            {{ card.value }}
          </div>
        </div>
        <div class="text-xs font-semibold text-[#1A2E22]">{{ card.label }}</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ card.sub }}</div>
      </div>
    </template>
  </div>

  <!-- ══ Accès rapides admin ══ -->
  <div v-if="authStore.isAdmin" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">

    <!-- Gestion utilisateurs -->
    <div class="bg-gradient-to-r from-[#2563EB] to-[#1e40af] rounded-2xl p-5
                flex items-center justify-between gap-4 shadow-lg">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
          👥
        </div>
        <div>
          <p class="font-serif text-sm font-bold text-white">Gérer les utilisateurs</p>
          <p class="text-xs text-white/70">Supprimer citoyens, agents et admins.</p>
        </div>
      </div>
      <router-link :to="{ name: 'admin-users' }"
        class="inline-flex items-center gap-1 bg-white text-[#2563EB] font-bold
               text-xs px-4 py-2 rounded-xl no-underline flex-shrink-0
               hover:-translate-y-0.5 transition-all shadow">
        Gérer →
      </router-link>
    </div>

    <!-- Gestion agents -->
    <div class="bg-gradient-to-r from-[#C41230] to-[#8B0D22] rounded-2xl p-5
                flex items-center justify-between gap-4 shadow-lg">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
          👮
        </div>
        <div>
          <p class="font-serif text-sm font-bold text-white">Gérer les agents</p>
          <p class="text-xs text-white/70">Créer et désactiver des comptes agents.</p>
        </div>
      </div>
      <router-link :to="{ name: 'admin-agents' }"
        class="inline-flex items-center gap-1 bg-white text-[#C41230] font-bold
               text-xs px-4 py-2 rounded-xl no-underline flex-shrink-0
               hover:-translate-y-0.5 transition-all shadow">
        Gérer →
      </router-link>
    </div>
  </div>

  <!-- ══ Graphiques ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Répartition par type</h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <canvas v-else id="donutChart" height="180"></canvas>
    </div>
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 lg:col-span-2">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Répartition par statut</h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <canvas v-else id="barChart" height="140"></canvas>
    </div>
  </div>

  <!-- ══ Catégories + Déclarations récentes ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Catégories actives</h2>
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 5" :key="i" class="skeleton h-8 rounded-lg"></div>
      </div>
      <div v-else-if="stats?.categories_populaires?.length" class="space-y-2">
        <div v-for="(cat, i) in stats.categories_populaires" :key="cat.libelle"
          class="flex items-center gap-2">
          <span class="text-xs font-bold text-[#005A3C] w-4">{{ i + 1 }}</span>
          <div class="flex-1 min-w-0">
            <div class="text-xs font-medium text-[#1A2E22] truncate">{{ cat.libelle }}</div>
            <div class="h-1 bg-gray-100 rounded-full mt-1">
              <div class="h-full bg-[#005A3C] rounded-full"
                :style="{ width: `${Math.min(100, (cat.nombre / (stats.total_declarations || 1)) * 100)}%` }">
              </div>
            </div>
          </div>
          <span class="text-xs font-bold text-gray-500">{{ cat.nombre }}</span>
        </div>
      </div>
      <p v-else class="text-xs text-gray-400">Aucune donnée.</p>
    </div>

    <div class="lg:col-span-2 bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-serif text-sm font-bold text-[#1A2E22]">Déclarations récentes</h2>
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
          class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-all cursor-pointer">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
            :style="{ backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold text-[#005A3C] truncate">
                {{ decl.numero_piece }}
              </span>
              <span class="badge text-[10px] flex-shrink-0"
                :style="{ color: getStatus(decl.statut).color, backgroundColor: getStatus(decl.statut).bg }">
                {{ getStatus(decl.statut).label }}
              </span>
            </div>
            <div class="flex gap-2 text-[10px] text-gray-400 mt-0.5">
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