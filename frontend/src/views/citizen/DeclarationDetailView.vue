<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const route     = useRoute()
const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declaration  = ref(null)
const loading      = ref(true)
const apiError     = ref(null)
const downloading  = ref(false)

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await declarationsAPI.detail(route.params.id)
    declaration.value = data
  } catch (e) {
    apiError.value = e.response?.status === 404
      ? 'Cette déclaration est introuvable.'
      : 'Impossible de charger la déclaration.'
  } finally {
    loading.value = false
  }
})

/* ══ PDF ══ */
const downloadPDF = async () => {
  downloading.value = true
  try {
    const { data } = await declarationsAPI.downloadPDF(declaration.value.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${declaration.value.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    apiError.value = 'Impossible de générer le PDF.'
  } finally {
    downloading.value = false
  }
}

/* ══ Helpers ══ */
const statusFlow = [
  { key: 'EN_ATTENTE', label: 'En attente',  icon: '⏳', desc: 'Déclaration reçue, en cours de traitement.' },
  { key: 'VALIDE',     label: 'Validée',      icon: '✅', desc: 'Validée par nos services, matching actif.' },
  { key: 'RETROUVE',   label: 'Retrouvée',    icon: '🎉', desc: 'Une correspondance a été trouvée !' },
  { key: 'RESTITUE',   label: 'Restituée',    icon: '🤝', desc: 'La pièce a été restituée à son propriétaire.' },
]
const negativeStatus = ['REJETE', 'CLOTURE']

const statusConfig = {
  EN_ATTENTE: { label: 'En attente',  color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',      color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',    color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',    color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',      color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',     color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const statusIndex = computed(() => {
  if (!declaration.value) return -1
  return statusFlow.findIndex(s => s.key === declaration.value.statut)
})

const isNegative = computed(() =>
  declaration.value && negativeStatus.includes(declaration.value.statut)
)

const formatDate = (d, withTime = false) => {
  if (!d) return '—'
  const opts = { day: '2-digit', month: 'long', year: 'numeric' }
  if (withTime) Object.assign(opts, { hour: '2-digit', minute: '2-digit' })
  return new Date(d).toLocaleDateString('fr-FR', opts)
}

const hasMatch = computed(() =>
  declaration.value?.declaration_correspondante ||
  declaration.value?.correspondance_detail
)
const match = computed(() =>
  declaration.value?.correspondance_detail || declaration.value?.declaration_correspondante
)
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-3xl mx-auto">

  <!-- ══ Navigation ══ -->
  <div class="flex items-center gap-3 mb-6">
    <button @click="router.back()"
      class="flex items-center gap-1.5 text-xs text-gray-400 hover:text-[#005A3C]
             bg-transparent border-none cursor-pointer transition-colors">
      ← Retour
    </button>
    <span class="text-gray-300">·</span>
    <span class="text-xs text-gray-400">Détail de la déclaration</span>
  </div>

  <!-- ══ Chargement ══ -->
  <div v-if="loading" class="space-y-4">
    <div class="skeleton h-32 rounded-2xl"></div>
    <div class="skeleton h-64 rounded-2xl"></div>
    <div class="skeleton h-48 rounded-2xl"></div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-else-if="apiError && !declaration"
    class="text-center py-20 bg-white rounded-2xl shadow-card">
    <div class="text-4xl mb-4">😕</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">{{ apiError }}</p>
    <button @click="router.back()"
      class="mt-4 text-sm text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      ← Retour à mes déclarations
    </button>
  </div>

  <!-- ══ Contenu ══ -->
  <template v-else-if="declaration">

    <!-- ─── Carte héro ─── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 mb-5 overflow-hidden">

      <!-- Bande colorée en haut -->
      <div class="h-1.5"
        :style="{
          backgroundColor: isNegative ? '#DC2626'
            : declaration.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
        }">
      </div>

      <div class="p-6">
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <!-- Icône type -->
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-3xl flex-shrink-0"
              :style="{
                backgroundColor: declaration.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
              }">
              {{ declaration.type_declaration === 'PERTE' ? '😟' : '🤲' }}
            </div>
            <div>
              <div class="flex items-center gap-2 mb-1 flex-wrap">
                <span class="font-bold text-xs px-2 py-1 rounded"
                  :style="{
                    backgroundColor: declaration.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
                    color: declaration.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
                  }">
                  {{ declaration.type_declaration }}
                </span>
                <span class="badge text-xs"
                  :style="{
                    color: getStatus(declaration.statut).color,
                    backgroundColor: getStatus(declaration.statut).bg
                  }">
                  {{ getStatus(declaration.statut).label }}
                </span>
              </div>
              <h1 class="font-serif text-xl font-bold text-[#1A2E22] leading-tight">
                <span v-if="declaration.nom_declarant">
                  {{ declaration.nom_declarant }}
                  <span class="font-normal">{{ declaration.prenom_declarant }}</span>
                </span>
                <span v-else>{{ declaration.nom_sur_piece }}</span>
              </h1>
              <div class="font-mono text-sm font-bold text-[#005A3C] tracking-wider mt-0.5">
                {{ declaration.numero_piece }}
              </div>
            </div>
          </div>

          <!-- Bouton PDF -->
          <button @click="downloadPDF" :disabled="downloading"
            class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                   text-xs px-4 py-2.5 rounded-xl border-none cursor-pointer
                   transition-all hover:bg-[#007A52] hover:shadow-md
                   disabled:opacity-50 flex-shrink-0">
            <span v-if="downloading" class="loader-dot-xs"></span>
            <span v-else>📄</span>
            {{ downloading ? 'Génération…' : 'Récépissé PDF' }}
          </button>
        </div>

        <!-- Numéro récépissé -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 text-xs text-gray-400">
          <span>📋 Récépissé :</span>
          <span class="font-mono font-bold text-gray-600">{{ declaration.numero_recepisse }}</span>
          <span class="mx-2">·</span>
          <span>Déclaré le {{ formatDate(declaration.date_declaration, true) }}</span>
        </div>
      </div>
    </div>

    <!-- ─── Alerte match ─── -->
    <transition name="slide-in">
      <div v-if="hasMatch"
        class="bg-green-50 border-2 border-green-300 rounded-2xl p-5 mb-5">
        <div class="flex items-start gap-3">
          <span class="text-2xl">🎉</span>
          <div>
            <p class="font-bold text-green-800 mb-1">
              {{ declaration.type_declaration === 'PERTE'
                ? 'Votre pièce a peut-être été retrouvée !'
                : 'Cette trouvaille correspond à une déclaration de perte !' }}
            </p>
            <p class="text-sm text-green-700 mb-3">
              Une correspondance automatique a été détectée.
              Rapprochez-vous du commissariat pour finaliser la restitution.
            </p>
            <!-- Carte match -->
            <div class="bg-white rounded-xl p-4 border border-green-200 flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center text-lg"
                :style="{
                  backgroundColor: match?.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
                }">
                {{ match?.type_declaration === 'PERTE' ? '😟' : '🤲' }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-mono text-xs font-bold text-[#005A3C] tracking-wider">
                  {{ match?.numero_piece }}
                </div>
                <div class="text-xs text-gray-600">{{ match?.nom_sur_piece }}</div>
                <div class="text-xs text-gray-400 mt-0.5">{{ match?.numero_recepisse }}</div>
              </div>
              <span class="text-xs text-green-600 font-semibold bg-green-100 px-2 py-1 rounded-lg">
                {{ match?.type_declaration === 'PERTE' ? 'Perte' : 'Trouvaille' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ─── Remarques admin ─── -->
    <div v-if="declaration.remarques_admin"
      class="bg-blue-50 border border-blue-200 rounded-2xl p-4 mb-5 flex items-start gap-3">
      <span class="text-lg">💬</span>
      <div>
        <p class="text-xs font-bold text-blue-800 mb-1">Message du service</p>
        <p class="text-sm text-blue-700">{{ declaration.remarques_admin }}</p>
      </div>
    </div>

    <!-- ─── Fiche détaillée ─── -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">

      <!-- Informations pièce -->
      <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
        <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-4 flex items-center gap-2">
          <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">🪪</span>
          Pièce concernée
        </h2>
        <dl class="space-y-3 text-sm">
          <div v-for="row in [
            { label: 'Catégorie',          value: declaration.categorie_detail?.libelle || declaration.categorie_nom || '—' },
            { label: 'Numéro',             value: declaration.numero_piece || 'Non communiqué', mono: !declaration.numero_piece },
            { label: 'Nom de famille',     value: declaration.nom_declarant   || '—' },
            { label: 'Prénom(s)',          value: declaration.prenom_declarant || '—' },
            { label: 'Date de naissance',  value: declaration.date_naissance
                                                  ? new Date(declaration.date_naissance + 'T00:00:00').toLocaleDateString('fr-FR') : '—' },
            { label: 'Lieu de naissance',  value: declaration.lieu_naissance  || '—' },
            { label: 'Profession',         value: declaration.profession       || '—' },
            { label: 'Date de la ' + (declaration.type_declaration === 'PERTE' ? 'perte' : 'trouvaille'),
                                           value: formatDate(declaration.date_perte) },
            { label: 'Lieu',               value: declaration.lieu_perte       || '—' },
          ]" :key="row.label">
            <div class="flex justify-between gap-2">
              <dt class="text-xs text-gray-400 font-medium flex-shrink-0">{{ row.label }}</dt>
              <dd :class="['text-right font-medium text-[#1A2E22] break-all',
                           row.mono && 'font-mono text-[#005A3C] tracking-wide text-xs']">
                {{ row.value }}
              </dd>
            </div>
            <div class="h-px bg-gray-50"></div>
          </div>
        </dl>
      </div>

      <!-- Photo si disponible + Infos déclarant -->
      <div class="space-y-4">
        <div v-if="declaration.photo_piece"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-4 text-center">
          <p class="text-xs text-gray-400 mb-2 font-medium">Photo de la pièce</p>
          <img :src="declaration.photo_piece" alt="Photo pièce"
            class="max-h-32 w-auto mx-auto rounded-xl object-cover shadow-sm"/>
        </div>

        <!-- Description -->
        <div v-if="declaration.description"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
          <h3 class="font-serif text-sm font-bold text-[#1A2E22] mb-2">Description</h3>
          <p class="text-sm text-gray-600 leading-relaxed">
            {{ declaration.description }}
          </p>
        </div>

        <!-- Dates -->
        <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
          <h3 class="font-serif text-sm font-bold text-[#1A2E22] mb-3">Horodatage</h3>
          <div class="space-y-2 text-xs">
            <div class="flex justify-between">
              <span class="text-gray-400">Déclaré le</span>
              <span class="font-medium text-[#1A2E22]">{{ formatDate(declaration.date_declaration, true) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Dernière mise à jour</span>
              <span class="font-medium text-[#1A2E22]">{{ formatDate(declaration.date_modification, true) }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ─── Timeline de statut ─── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 mb-5">
      <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
        <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">📊</span>
        Progression
      </h2>

      <!-- Statut négatif -->
      <div v-if="isNegative"
        class="flex items-center gap-3 bg-red-50 rounded-xl p-4 text-sm">
        <span class="text-2xl">{{ declaration.statut === 'REJETE' ? '❌' : '🔒' }}</span>
        <div>
          <p class="font-bold text-rouge">{{ getStatus(declaration.statut).label }}</p>
          <p class="text-xs text-red-600 mt-0.5">
            {{ declaration.statut === 'REJETE'
              ? 'Cette déclaration a été rejetée. Contactez le service pour plus d\'informations.'
              : 'Cette déclaration a été clôturée.' }}
          </p>
        </div>
      </div>

      <!-- Timeline normale -->
      <div v-else class="relative">
        <!-- Ligne de connexion -->
        <div class="absolute left-[18px] top-[18px] bottom-[18px] w-0.5 bg-gray-200 -z-0"></div>

        <div class="space-y-0">
          <div v-for="(s, i) in statusFlow" :key="s.key"
            class="flex items-start gap-4 relative pb-6 last:pb-0">

            <!-- Point timeline -->
            <div :class="[
              'w-9 h-9 rounded-full flex items-center justify-center text-sm flex-shrink-0 relative z-10 border-2 transition-all',
              i < statusIndex || i === statusIndex
                ? 'border-[#005A3C] bg-[#005A3C] text-white shadow-md'
                : 'border-gray-200 bg-white text-gray-400'
            ]">
              <span v-if="i < statusIndex">✓</span>
              <span v-else>{{ s.icon }}</span>
            </div>

            <!-- Contenu -->
            <div :class="['pt-1.5', i > statusIndex && 'opacity-40']">
              <p :class="[
                'text-sm font-semibold',
                i <= statusIndex ? 'text-[#1A2E22]' : 'text-gray-400'
              ]">
                {{ s.label }}
                <span v-if="i === statusIndex"
                  class="ml-2 inline-block bg-[#005A3C]/10 text-[#005A3C]
                         text-xs font-bold px-2 py-0.5 rounded-full">
                  Étape actuelle
                </span>
              </p>
              <p class="text-xs text-gray-500 mt-0.5">{{ s.desc }}</p>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- ─── Erreur ─── -->
    <div v-if="apiError"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️</span><span>{{ apiError }}</span>
    </div>

    <!-- ─── Actions bas de page ─── -->
    <div class="flex items-center justify-between gap-3 flex-wrap">
      <router-link :to="{ name: 'mes-declarations' }"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-gray-500
               bg-white border border-gray-200 px-5 py-3 rounded-xl no-underline
               hover:bg-gray-50 transition-all">
        ← Toutes mes déclarations
      </router-link>
      <div class="flex items-center gap-2">
        <button @click="downloadPDF" :disabled="downloading"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-5 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:shadow-md
                 disabled:opacity-50">
          <span v-if="downloading" class="loader-dot-xs"></span>
          <span v-else>📄</span>
          Télécharger PDF
        </button>
        <router-link :to="{ name: 'declare' }"
          class="inline-flex items-center gap-1.5 text-sm font-semibold
                 text-[#005A3C] bg-[#E8F4F0] px-5 py-3 rounded-xl no-underline
                 hover:bg-[#d0ece3] transition-all">
          + Nouvelle déclaration
        </router-link>
      </div>
    </div>

  </template>

</div>
</div>
</template>

<style scoped>
.slide-in-enter-active { transition: all .4s cubic-bezier(.175,.885,.32,1.275); }
.slide-in-enter-from   { opacity: 0; transform: translateY(-10px) scale(.97); }

.loader-dot-xs {
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>