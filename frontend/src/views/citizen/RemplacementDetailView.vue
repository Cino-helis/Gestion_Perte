<script setup>
/**
 * RemplacementDetailView.vue
 * Suivi complet d'un dossier de remplacement par le citoyen.
 * Route : /remplacement/:id   (id = DemandeRemplacement.id)
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { remplacementsAPI } from '../../services/api'

const route  = useRoute()
const router = useRouter()

const demande   = ref(null)
const loading   = ref(true)
const apiError  = ref(null)
const downloading = ref(false)

onMounted(async () => {
  try {
    const { data } = await remplacementsAPI.detail(route.params.id)
    demande.value = data
  } catch (e) {
    apiError.value = e.response?.status === 404
      ? 'Ce dossier est introuvable ou ne vous appartient pas.'
      : 'Impossible de charger le dossier.'
  } finally {
    loading.value = false
  }
})

// ── Téléchargement de l'autorisation PDF ───────────────────────────────────
const downloadPDF = async () => {
  downloading.value = true
  try {
    const { data } = await remplacementsAPI.downloadAutorisation(demande.value.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a   = document.createElement('a')
    a.href     = url
    a.download = `autorisation_${demande.value.numero_dossier}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Impossible de générer le PDF.'
  } finally {
    downloading.value = false
  }
}

// ── Timeline des étapes ─────────────────────────────────────────────────────
const ETAPES = [
  {
    key:   'EN_ATTENTE',
    label: 'Dossier ouvert',
    icon:  '📂',
    color: '#D97706',
    desc:  'Votre dossier a été ouvert. Un agent va l\'examiner très prochainement.',
  },
  {
    key:   'RECEPISSE_EMIS',
    label: 'Autorisation émise',
    icon:  '📄',
    color: '#2563EB',
    desc:  'Votre autorisation officielle est prête. Téléchargez-la et rendez-vous au commissariat désigné.',
  },
  {
    key:   'EN_TRAITEMENT',
    label: 'En traitement',
    icon:  '⚙️',
    color: '#7C3AED',
    desc:  'Votre dossier est en cours de traitement au commissariat. Fabrication de la pièce en cours.',
  },
  {
    key:   'DOCUMENT_PRET',
    label: 'Pièce prête',
    icon:  '🎉',
    color: '#059669',
    desc:  'Votre nouvelle pièce est prête ! Rendez-vous au commissariat pour la retirer.',
  },
  {
    key:   'RETIRE',
    label: 'Retiré',
    icon:  '✅',
    color: '#065F46',
    desc:  'Procédure terminée. Votre pièce a été remise.',
  },
]

const STATUTS_POSITIFS = ['EN_ATTENTE', 'RECEPISSE_EMIS', 'EN_TRAITEMENT', 'DOCUMENT_PRET', 'RETIRE']

const currentStep = computed(() => {
  if (!demande.value) return -1
  return ETAPES.findIndex(e => e.key === demande.value.statut)
})

const isAnnule = computed(() => demande.value?.statut === 'ANNULE')

const currentEtape = computed(() => {
  if (!demande.value || isAnnule.value) return null
  return ETAPES[currentStep.value] || null
})

const statusConfig = {
  EN_ATTENTE:     { label: 'En attente',            color: '#D97706', bg: '#FEF3C7' },
  RECEPISSE_EMIS: { label: 'Autorisation émise',    color: '#2563EB', bg: '#DBEAFE' },
  EN_TRAITEMENT:  { label: 'En traitement',          color: '#7C3AED', bg: '#EDE9FE' },
  DOCUMENT_PRET:  { label: 'Pièce prête',           color: '#059669', bg: '#D1FAE5' },
  RETIRE:         { label: 'Retiré',                color: '#065F46', bg: '#A7F3D0' },
  ANNULE:         { label: 'Annulé',                color: '#DC2626', bg: '#FEE2E2' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d, withTime = false) => {
  if (!d) return '—'
  const opts = { day: '2-digit', month: 'long', year: 'numeric' }
  if (withTime) Object.assign(opts, { hour: '2-digit', minute: '2-digit' })
  return new Date(d).toLocaleDateString('fr-FR', opts)
}

// Documents à fournir au commissariat
const DOCUMENTS = [
  'L\'autorisation officielle DéclaTogo (ce document)',
  `Le récépissé de perte original`,
  'Une pièce d\'identité valide (ou document officiel)',
  'Une photo d\'identité récente (format passeport)',
  'Le timbre fiscal réglementaire (se renseigner au commissariat)',
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-3xl mx-auto">

  <!-- ══ Navigation ══ -->
  <div class="flex items-center gap-3 mb-6">
    <button @click="router.push({ name: 'mes-declarations' })"
      class="flex items-center gap-1.5 text-xs text-gray-400 hover:text-[#005A3C]
             bg-transparent border-none cursor-pointer transition-colors">
      ← Mes déclarations
    </button>
    <span class="text-gray-300">·</span>
    <span class="text-xs text-gray-400">Dossier de remplacement</span>
  </div>

  <!-- ══ Chargement ══ -->
  <div v-if="loading" class="space-y-4">
    <div class="skeleton h-36 rounded-2xl"></div>
    <div class="skeleton h-80 rounded-2xl"></div>
    <div class="skeleton h-48 rounded-2xl"></div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-else-if="apiError && !demande"
    class="text-center py-20 bg-white rounded-2xl shadow-card">
    <div class="text-4xl mb-4">😕</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">{{ apiError }}</p>
    <button @click="router.push({ name: 'mes-declarations' })"
      class="mt-4 text-sm text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      ← Retour à mes déclarations
    </button>
  </div>

  <template v-else-if="demande">

    <!-- ── Annulé ── -->
    <div v-if="isAnnule"
      class="bg-red-50 border-2 border-red-200 rounded-2xl p-6 mb-5 text-center">
      <div class="text-4xl mb-3">❌</div>
      <h2 class="font-serif text-xl font-bold text-rouge mb-2">Dossier annulé</h2>
      <p class="text-sm text-red-600">
        Ce dossier de remplacement a été annulé.
        Contactez le service DéclaTogo pour plus d'informations.
      </p>
      <p v-if="demande.remarques" class="text-xs text-gray-500 mt-2 italic">
        Note : {{ demande.remarques }}
      </p>
    </div>

    <!-- ── Carte héro ── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 mb-5 overflow-hidden">
      <!-- Barre de progression colorée -->
      <div class="h-2 bg-gray-100 relative">
        <div class="h-full rounded-r-full transition-all duration-700"
          :style="{
            width: `${demande.progression_pct}%`,
            backgroundColor: currentEtape?.color || '#D97706'
          }">
        </div>
      </div>

      <div class="p-6">
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <div class="flex items-center gap-2 mb-2 flex-wrap">
              <span class="badge text-xs font-bold"
                :style="{ color: getStatus(demande.statut).color, backgroundColor: getStatus(demande.statut).bg }">
                {{ currentEtape?.icon || '❌' }} {{ getStatus(demande.statut).label }}
              </span>
              <span class="text-xs text-gray-400">{{ demande.progression_pct }}% complété</span>
            </div>
            <h1 class="font-serif text-xl font-bold text-[#1A2E22] mb-0.5">
              Dossier de remplacement
            </h1>
            <div class="font-mono text-base font-bold text-[#005A3C] tracking-wider">
              {{ demande.numero_dossier }}
            </div>
            <p class="text-xs text-gray-400 mt-1.5">
              Ouvert le {{ formatDate(demande.date_creation, true) }}
            </p>
          </div>

          <!-- Bouton téléchargement autorisation -->
          <div class="flex flex-col gap-2 flex-shrink-0">
            <button v-if="demande.autorisation_disponible"
              @click="downloadPDF" :disabled="downloading"
              class="flex items-center gap-2 bg-[#2563EB] text-white font-bold
                     text-xs px-4 py-3 rounded-xl border-none cursor-pointer
                     transition-all hover:bg-[#1d4ed8] hover:shadow-md
                     disabled:opacity-50 whitespace-nowrap">
              <span v-if="downloading" class="loader-dot-xs"></span>
              <span v-else>📄</span>
              {{ downloading ? 'Génération…' : 'Télécharger l\'autorisation PDF' }}
            </button>
            <p v-else class="text-xs text-gray-400 text-center max-w-[180px]">
              L'autorisation sera disponible dès qu'un agent l'aura émise.
            </p>
          </div>
        </div>

        <!-- Réf. déclaration de perte -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-3 text-xs text-gray-400 flex-wrap">
          <span>📋 Perte réf. : <strong class="font-mono text-gray-600">{{ demande.declaration_recepisse }}</strong></span>
          <span>·</span>
          <span>📁 {{ demande.declaration_categorie }}</span>
          <span>·</span>
          <span>👤 {{ demande.declaration_nom }}</span>
        </div>
      </div>
    </div>

    <!-- ── Alerte contextuelle selon statut ── -->
    <transition name="slide-in">
      <div v-if="demande.statut === 'RECEPISSE_EMIS'"
        class="bg-blue-50 border-2 border-blue-300 rounded-2xl p-5 mb-5">
        <div class="flex items-start gap-3">
          <span class="text-2xl">📄</span>
          <div>
            <p class="font-bold text-blue-800 mb-1">Votre autorisation est prête !</p>
            <p class="text-sm text-blue-700 mb-3 leading-relaxed">
              Téléchargez l'autorisation PDF et rendez-vous au commissariat désigné
              avec les documents listés ci-dessous.
            </p>
            <button @click="downloadPDF" :disabled="downloading"
              class="flex items-center gap-2 bg-[#2563EB] text-white font-bold
                     text-xs px-4 py-2.5 rounded-xl border-none cursor-pointer
                     hover:bg-[#1d4ed8] transition-all disabled:opacity-50">
              <span v-if="downloading" class="loader-dot-xs"></span>
              <span v-else>📥</span>
              {{ downloading ? 'Génération…' : 'Télécharger maintenant' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="demande.statut === 'DOCUMENT_PRET'"
        class="bg-green-50 border-2 border-green-300 rounded-2xl p-5 mb-5">
        <div class="flex items-start gap-3">
          <span class="text-2xl">🎉</span>
          <div>
            <p class="font-bold text-green-800 mb-1">Votre pièce est prête à être retirée !</p>
            <p class="text-sm text-green-700 leading-relaxed">
              Rendez-vous au commissariat
              <strong>{{ demande.commissariat || 'désigné' }}</strong>
              en apportant votre autorisation PDF et votre récépissé de dépôt.
            </p>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Erreur ── -->
    <div v-if="apiError"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null" class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>

    <!-- ── Timeline ── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 mb-5">
      <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-6 flex items-center gap-2">
        <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">📊</span>
        Progression de votre dossier
      </h2>

      <div v-if="isAnnule" class="text-center py-4 text-rouge text-sm">
        ❌ Ce dossier a été annulé.
      </div>

      <div v-else class="relative">
        <!-- Ligne verticale de connexion -->
        <div class="absolute left-[18px] top-5 bottom-5 w-0.5 bg-gray-200"></div>

        <div class="space-y-0">
          <div v-for="(etape, i) in ETAPES" :key="etape.key"
            class="flex items-start gap-4 relative pb-7 last:pb-0">

            <!-- Point de la timeline -->
            <div :class="[
              'w-9 h-9 rounded-full flex items-center justify-center text-sm flex-shrink-0',
              'relative z-10 border-2 transition-all duration-500',
              i < currentStep
                ? 'border-[#005A3C] bg-[#005A3C] text-white shadow-md'
                : i === currentStep
                  ? 'border-2 text-white shadow-lg scale-110'
                  : 'border-gray-200 bg-white text-gray-400'
            ]"
            :style="i === currentStep ? {
              borderColor: etape.color,
              backgroundColor: etape.color,
            } : {}">
              <span v-if="i < currentStep" class="text-xs">✓</span>
              <span v-else>{{ etape.icon }}</span>
            </div>

            <!-- Contenu de l'étape -->
            <div :class="['pt-1 flex-1', i > currentStep && 'opacity-40']">
              <div class="flex items-center gap-2 flex-wrap mb-0.5">
                <p :class="[
                  'text-sm font-semibold',
                  i <= currentStep ? 'text-[#1A2E22]' : 'text-gray-400'
                ]">
                  {{ etape.label }}
                </p>
                <span v-if="i === currentStep && !isAnnule"
                  class="text-[10px] font-bold px-2 py-0.5 rounded-full text-white"
                  :style="{ backgroundColor: etape.color }">
                  Étape actuelle
                </span>
                <!-- Date de l'étape si disponible -->
                <span v-if="i === 0 && demande.date_creation" class="text-[10px] text-gray-400 ml-auto">
                  {{ formatDate(demande.date_creation) }}
                </span>
                <span v-if="i === 1 && demande.date_emission_recepisse" class="text-[10px] text-gray-400 ml-auto">
                  {{ formatDate(demande.date_emission_recepisse) }}
                </span>
                <span v-if="i === 2 && demande.date_depot_commissariat" class="text-[10px] text-gray-400 ml-auto">
                  {{ formatDate(demande.date_depot_commissariat) }}
                </span>
                <span v-if="i === 3 && demande.date_document_pret" class="text-[10px] text-gray-400 ml-auto">
                  {{ formatDate(demande.date_document_pret) }}
                </span>
                <span v-if="i === 4 && demande.date_retrait" class="text-[10px] text-gray-400 ml-auto">
                  {{ formatDate(demande.date_retrait) }}
                </span>
              </div>
              <p class="text-xs text-gray-500 leading-relaxed">{{ etape.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Commissariat désigné ── -->
    <div v-if="demande.commissariat"
      class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 mb-5">
      <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-4 flex items-center gap-2">
        <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">🏛️</span>
        Commissariat agréé
      </h2>
      <div class="space-y-2.5 text-sm">
        <div class="flex items-start gap-3">
          <span class="text-gray-400 text-xs mt-0.5 w-6">🏛️</span>
          <div>
            <p class="font-bold text-[#1A2E22]">{{ demande.commissariat }}</p>
          </div>
        </div>
        <div v-if="demande.adresse_commissariat" class="flex items-start gap-3">
          <span class="text-gray-400 text-xs mt-0.5 w-6">📍</span>
          <p class="text-gray-600 text-sm">{{ demande.adresse_commissariat }}</p>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-gray-400 text-xs mt-0.5 w-6">🕐</span>
          <p class="text-gray-600 text-sm">{{ demande.horaires_commissariat || 'Lun.–Ven. 08h00–16h00' }}</p>
        </div>
      </div>
    </div>
    <div v-else-if="demande.statut !== 'EN_ATTENTE' && demande.statut !== 'ANNULE'"
      class="bg-yellow-50 border border-yellow-200 rounded-2xl p-4 mb-5">
      <p class="text-sm text-yellow-700">
        ℹ️ Le commissariat agréé vous sera communiqué très prochainement.
        Consultez vos notifications ou revenez sur cette page.
      </p>
    </div>

    <!-- ── Documents à fournir ── -->
    <div v-if="['RECEPISSE_EMIS', 'EN_TRAITEMENT'].includes(demande.statut)"
      class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 mb-5">
      <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-4 flex items-center gap-2">
        <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">📋</span>
        Documents à présenter au commissariat
      </h2>
      <ol class="space-y-2 list-none pl-0">
        <li v-for="(doc, i) in DOCUMENTS" :key="i"
          class="flex items-start gap-3 text-sm">
          <span class="w-6 h-6 rounded-full bg-[#005A3C] text-white text-xs
                        flex items-center justify-center flex-shrink-0 font-bold mt-0.5">
            {{ i + 1 }}
          </span>
          <span class="text-gray-600 leading-relaxed">
            {{ i === 1 ? `Le récépissé de perte original N° ${demande.declaration_recepisse}` : doc }}
          </span>
        </li>
      </ol>
    </div>

    <!-- ── Remarques de l'agent ── -->
    <div v-if="demande.remarques"
      class="bg-blue-50 border border-blue-200 rounded-2xl p-4 mb-5 flex items-start gap-3">
      <span class="text-lg">💬</span>
      <div>
        <p class="text-xs font-bold text-blue-800 mb-1">Note de l'agent</p>
        <p class="text-sm text-blue-700">{{ demande.remarques }}</p>
      </div>
    </div>

    <!-- ── Traité par ── -->
    <div v-if="demande.traite_par_nom"
      class="text-xs text-gray-400 text-center mb-5">
      Dossier traité par <strong class="text-gray-500">{{ demande.traite_par_nom }}</strong>
    </div>

    <!-- ── Actions bas ── -->
    <div class="flex items-center justify-between gap-3 flex-wrap">
      <router-link :to="{ name: 'declaration-detail', params: { id: demande.declaration } }"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-gray-500
               bg-white border border-gray-200 px-5 py-3 rounded-xl no-underline
               hover:bg-gray-50 transition-all">
        ← Voir la déclaration de perte
      </router-link>

      <button v-if="demande.autorisation_disponible"
        @click="downloadPDF" :disabled="downloading"
        class="flex items-center gap-2 bg-[#2563EB] text-white font-bold
               text-sm px-5 py-3 rounded-xl border-none cursor-pointer
               transition-all hover:bg-[#1d4ed8] hover:shadow-md disabled:opacity-50">
        <span v-if="downloading" class="loader-dot-xs"></span>
        <span v-else>📄</span>
        Télécharger l'autorisation PDF
      </button>
    </div>

  </template>

</div>
</div>
</template>

<style scoped>
.slide-in-enter-active { transition: all .35s cubic-bezier(.175,.885,.32,1.275); }
.slide-in-enter-from   { opacity: 0; transform: translateY(-8px) scale(.98); }

.loader-dot-xs {
  display: inline-block; width: 12px; height: 12px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
