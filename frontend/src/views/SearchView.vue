<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { declarationsAPI, categoriesAPI } from '../services/api'

const route  = useRoute()
const router = useRouter()

/* ══ État ══ */
const query      = ref(route.query.q    || '')
const catFilter  = ref(route.query.cat  || '')
const results    = ref([])
const categories = ref([])
const loading    = ref(false)
const searched   = ref(false)
let   debounce   = null

/* ══ Chargement catégories ══ */
onMounted(async () => {
  try {
    const { data } = await categoriesAPI.list()
    categories.value = data.results ?? data
  } catch {}
  // Lancer la recherche si query dans l'URL
  if (query.value) doSearch()
})

/* ══ Recherche debounced ══ */
const doSearch = async () => {
  if (!query.value.trim()) { results.value = []; searched.value = false; return }
  loading.value = true
  searched.value = true
  try {
    const payload = { numero_piece: query.value.trim() }
    if (catFilter.value) payload.categorie = Number(catFilter.value)
    const { data } = await declarationsAPI.rechercher(payload)
    results.value = data.correspondances ?? []
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
  // Sync URL
  router.replace({ query: { q: query.value, cat: catFilter.value || undefined }})
}

watch([query, catFilter], () => {
  clearTimeout(debounce)
  debounce = setTimeout(doSearch, 420)
})

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
  ? new Date(d).toLocaleDateString('fr-FR', { day:'2-digit', month:'short', year:'numeric' })
  : '—'

const popular = ['CNI', 'Passeport', 'Carte grise', 'Permis', 'Diplôme']
</script>

<template>
<div class="min-h-screen" style="background:#FAF7F2">

  <!-- ══ Hero barre de recherche ══ -->
  <section class="relative overflow-hidden py-16 px-[5%]"
           style="background-color:#005A3C">
    <div class="absolute inset-0 kente-bg opacity-30"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-transparent to-[#001a0e]/50"></div>

    <div class="relative z-10 max-w-2xl mx-auto text-center">
      <div class="inline-flex items-center gap-2 bg-white/10 text-[#D4A017]
                  border border-white/20 px-3 py-1.5 rounded-full text-xs font-bold mb-4">
        🔍 Recherche publique
      </div>
      <h1 class="font-serif text-[clamp(1.8rem,3vw,2.6rem)] font-bold text-white mb-3 leading-tight">
        Votre pièce a peut-être<br/>
        <span class="text-[#D4A017]">été retrouvée</span>
      </h1>
      <p class="text-white/75 text-sm mb-8 leading-relaxed">
        Saisissez le numéro de votre pièce perdue — nous cherchons dans toutes les trouvailles déclarées.
      </p>

      <!-- Barre de recherche principale -->
      <div class="bg-white rounded-2xl p-2 shadow-2xl flex flex-col sm:flex-row gap-2">
        <div class="relative flex-1">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            v-model="query"
            type="text"
            placeholder="Numéro de pièce (ex: TG20240001)"
            class="w-full border-0 outline-none bg-transparent pl-10 pr-4 py-3
                   text-sm text-[#1A2E22] placeholder:text-gray-400"
            @keyup.enter="doSearch"
          />
        </div>
        <select v-model="catFilter"
          class="border-0 outline-none bg-gray-50 rounded-xl text-sm text-gray-600
                 px-3 py-3 cursor-pointer min-w-[160px]">
          <option value="">Toutes catégories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.libelle }}</option>
        </select>
        <button @click="doSearch"
          class="bg-[#005A3C] text-white font-bold text-sm px-6 py-3 rounded-xl
                 border-none cursor-pointer transition-all hover:bg-[#007A52]
                 flex items-center gap-2">
          <span v-if="loading" class="loader-dot-sm"></span>
          <span v-else>🔍</span>
          Rechercher
        </button>
      </div>

      <!-- Recherches fréquentes -->
      <div class="flex items-center justify-center gap-2 flex-wrap mt-4">
        <span class="text-xs text-white/40">Fréquents :</span>
        <button v-for="chip in popular" :key="chip"
          @click="query = chip"
          class="bg-white/10 text-white/70 hover:bg-white/20 hover:text-white
                 text-xs px-3 py-1.5 rounded-full border border-white/15
                 transition-all cursor-pointer border-none">
          {{ chip }}
        </button>
      </div>
    </div>
  </section>


  <!-- ══ Zone de résultats ══ -->
  <section class="max-w-3xl mx-auto px-4 py-10">

    <!-- Pas encore recherché -->
    <div v-if="!searched && !loading" class="text-center py-16">
      <div class="text-5xl mb-4">🗂️</div>
      <p class="text-gray-400 text-sm">
        Entrez un numéro de pièce pour lancer la recherche.
      </p>
      <p class="text-xs text-gray-400 mt-2">
        La recherche porte sur toutes les trouvailles validées dans notre base.
      </p>
    </div>

    <!-- Chargement -->
    <div v-else-if="loading" class="space-y-3">
      <div class="flex items-center gap-3 mb-6">
        <div class="loader-ring"></div>
        <span class="text-sm text-gray-500">Recherche en cours…</span>
      </div>
      <div v-for="i in 3" :key="i" class="skeleton h-24 rounded-xl"></div>
    </div>

    <!-- Résultats -->
    <template v-else-if="searched">
      <!-- Header résultats -->
      <div class="flex items-center justify-between mb-5">
        <div>
          <span class="font-serif text-lg font-bold text-[#1A2E22]">
            {{ results.length }} résultat{{ results.length !== 1 ? 's' : '' }}
          </span>
          <span class="text-sm text-gray-400 ml-2">pour « {{ query }} »</span>
        </div>
        <button v-if="results.length || query"
          @click="query = ''; results = []; searched = false"
          class="text-xs text-gray-400 hover:text-[#C41230] bg-transparent
                 border-none cursor-pointer transition-colors">
          ✕ Effacer
        </button>
      </div>

      <!-- Aucun résultat -->
      <div v-if="results.length === 0"
        class="text-center py-14 bg-white rounded-2xl border border-gray-100 shadow-card">
        <div class="text-4xl mb-4">😕</div>
        <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
          Aucune trouvaille correspondante
        </p>
        <p class="text-sm text-gray-500 max-w-sm mx-auto mb-6 leading-relaxed">
          Votre pièce n'a pas encore été signalée. Déclarez votre perte pour être notifié
          dès qu'une correspondance apparaît.
        </p>
        <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
          class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-xl no-underline hover:bg-[#007A52] transition-all">
          📋 Déclarer ma perte
        </router-link>
      </div>

      <!-- Liste des trouvailles -->
      <div v-else class="space-y-3">
        <transition-group name="list-item">
          <div v-for="decl in results" :key="decl.id"
            class="bg-white rounded-2xl border border-gray-100 shadow-card
                   hover:shadow-card-lg hover:-translate-y-0.5 transition-all p-5
                   flex flex-col sm:flex-row items-start gap-4">

            <!-- Icône catégorie -->
            <div class="w-12 h-12 bg-[#E8F4F0] rounded-xl flex items-center
                        justify-center text-2xl flex-shrink-0">
              🤲
            </div>

            <!-- Infos -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 flex-wrap mb-1">
                <div>
                  <span class="font-mono font-bold text-[#005A3C] text-sm tracking-wider">
                    {{ decl.numero_piece }}
                  </span>
                  <span class="mx-2 text-gray-300">·</span>
                  <span class="text-sm font-semibold text-[#1A2E22]">
                    {{ decl.nom_sur_piece }}
                  </span>
                </div>
                <!-- Badge statut -->
                <span class="badge text-xs flex-shrink-0"
                  :style="{
                    color: getStatus(decl.statut).color,
                    backgroundColor: getStatus(decl.statut).bg
                  }">
                  {{ getStatus(decl.statut).label }}
                </span>
              </div>

              <div class="flex items-center gap-4 text-xs text-gray-400 flex-wrap mt-2">
                <span v-if="decl.categorie_nom">📁 {{ decl.categorie_nom }}</span>
                <span v-if="decl.lieu_perte">📍 {{ decl.lieu_perte }}</span>
                <span>📅 {{ formatDate(decl.date_declaration) }}</span>
              </div>
            </div>

            <!-- CTA -->
            <div class="flex-shrink-0 sm:self-center">
              <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
                class="inline-flex items-center gap-1.5 bg-[#005A3C] text-white
                       font-semibold text-xs px-4 py-2.5 rounded-xl no-underline
                       hover:bg-[#007A52] transition-all">
                ✅ C'est la mienne
              </router-link>
            </div>

          </div>
        </transition-group>

        <!-- Invite à déclarer quand même -->
        <div class="mt-6 bg-[#FFFBEB] border border-yellow-200 rounded-2xl p-5
                    flex items-start gap-3">
          <span class="text-xl">💡</span>
          <div>
            <p class="text-sm font-semibold text-yellow-800 mb-1">
              Vous ne trouvez pas votre pièce ?
            </p>
            <p class="text-xs text-yellow-700 leading-relaxed mb-3">
              Déclarez votre perte maintenant. Si votre pièce est signalée ultérieurement,
              vous recevrez une notification automatique.
            </p>
            <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
              class="inline-flex items-center gap-1.5 bg-yellow-600 text-white font-semibold
                     text-xs px-4 py-2 rounded-lg no-underline hover:bg-yellow-700 transition-all">
              📋 Déclarer ma perte
            </router-link>
          </div>
        </div>

      </div>
    </template>

  </section>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .3s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(12px); }

.loader-dot-sm {
  display: inline-block;
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
.loader-ring {
  width: 20px; height: 20px;
  border: 2px solid #e5e7eb;
  border-top-color: #005A3C;
  border-radius: 50%;
  animation: spin .8s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>