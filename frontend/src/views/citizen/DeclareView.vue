<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { declarationsAPI, categoriesAPI } from '../../services/api'

const route  = useRoute()
const router = useRouter()
const { t }  = useI18n()

/* ══════════════════════════════════════
   ÉTAT GLOBAL DU WIZARD
══════════════════════════════════════ */
const step           = ref(1)   // 1 | 2 | 3 | 4 (succès)
const submitting     = ref(false)
const apiError       = ref(null)
const createdDecl    = ref(null) // Déclaration créée après succès
const categories     = ref([])
const loadingCats    = ref(true)

/* ══════════════════════════════════════
   FORMULAIRE
══════════════════════════════════════ */
const form = ref({
  type_declaration: '',       // 'PERTE' | 'TROUVAILLE'
  categorie:        null,     // id numérique
  numero_piece:     '',       // optionnel
  nom:              '',       // Nom de famille — obligatoire
  prenom:           '',       // Prénom(s) — obligatoire
  date_naissance:   '',       // obligatoire
  lieu_naissance:   '',       // obligatoire
  profession:       '',       // obligatoire
  description:      '',
  lieu_perte:       '',
  date_perte:       '',
  photo_piece:      null,     // File object
})
const photoPreview = ref(null)
const isDragging   = ref(false)

/* ══════════════════════════════════════
   CATÉGORIES FALLBACK (si API hors ligne)
   Identiques à init_categories_windows.py
══════════════════════════════════════ */
const FALLBACK_CATEGORIES = [
  { id: 1, libelle: "Pièce d'identité",         icone: 'id-card'       },
  { id: 2, libelle: 'Véhicule',                 icone: 'car'           },
  { id: 3, libelle: 'Documents scolaires',      icone: 'graduation-cap'},
  { id: 4, libelle: 'Documents bancaires',      icone: 'credit-card'   },
  { id: 5, libelle: 'Documents professionnels', icone: 'briefcase'     },
  { id: 6, libelle: 'Documents de santé',       icone: 'heart'         },
  { id: 7, libelle: 'Autres documents',         icone: 'file'          },
]
const catsFromAPI = ref(false)

/* ══════════════════════════════════════
   PRÉ-REMPLIR LE TYPE DEPUIS LA QUERY
══════════════════════════════════════ */
onMounted(async () => {
  if (route.query.type === 'TROUVAILLE') form.value.type_declaration = 'TROUVAILLE'
  else if (route.query.type === 'PERTE') form.value.type_declaration = 'PERTE'

  try {
    const { data } = await categoriesAPI.list()
    const list = data.results ?? data
    if (list && list.length > 0) {
      categories.value = list
      catsFromAPI.value = true
    } else {
      categories.value = FALLBACK_CATEGORIES
    }
  } catch (e) {
    // API hors ligne → fallback silencieux
    categories.value = FALLBACK_CATEGORIES
  } finally {
    loadingCats.value = false
  }
})

/* ══════════════════════════════════════
   VALIDATION PAR ÉTAPE
══════════════════════════════════════ */
// Le bouton devient cliquable dès qu'un type est choisi
const step1Valid = computed(() => form.value.type_declaration !== '')
// Erreur affichée seulement si l'utilisateur clique sans catégorie
const catError = ref(false)
const step2Valid = computed(() => {
  const f = form.value
  return (
    f.nom.trim().length >= 2          &&
    f.prenom.trim().length >= 2       &&
    f.date_naissance !== ''           &&
    f.lieu_naissance.trim().length >= 2 &&
    f.profession.trim().length >= 2
  )
})

/* ══════════════════════════════════════
   NAVIGATION
══════════════════════════════════════ */
const goNext = () => {
  if (step.value === 1) {
    if (!form.value.categorie) { catError.value = true; return }
    catError.value = false
    step.value = 2
  } else if (step.value === 2 && step2Valid.value) {
    step.value = 3
  }
}
const goBack = () => {
  if (step.value > 1) step.value--
}

/* ══════════════════════════════════════
   GESTION PHOTO
══════════════════════════════════════ */
const handlePhotoChange = (e) => {
  const file = e.target.files?.[0] || e.dataTransfer?.files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    apiError.value = 'La photo ne doit pas dépasser 5 MB.'
    return
  }
  if (!['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
    apiError.value = 'Format non autorisé. Utilisez JPG ou PNG.'
    return
  }
  form.value.photo_piece = file
  const reader = new FileReader()
  reader.onload = (e) => { photoPreview.value = e.target.result }
  reader.readAsDataURL(file)
  apiError.value = null
}
const removePhoto = () => {
  form.value.photo_piece = null
  photoPreview.value = null
}
const handleDrop = (e) => {
  isDragging.value = false
  handlePhotoChange(e)
}

/* ══════════════════════════════════════
   SOUMISSION
══════════════════════════════════════ */
const handleSubmit = async () => {
  if (!step2Valid.value || !step1Valid.value) return
  submitting.value = true
  apiError.value   = null

  try {
    const formData = new FormData()
    // nom_sur_piece = "NOM Prénom" auto-construit côté backend
    // mais on l'envoie aussi pour compatibilité
    const nomSurPiece = `${form.value.nom.trim().toUpperCase()} ${form.value.prenom.trim()}`

    formData.append('type_declaration',  form.value.type_declaration)
    formData.append('categorie',         form.value.categorie)

    // Numéro de pièce — optionnel
    if (form.value.numero_piece.trim())
      formData.append('numero_piece', form.value.numero_piece.trim().toUpperCase())

    // nom_sur_piece : construit depuis nom + prénom
    formData.append('nom_sur_piece',     nomSurPiece)

    // Champs identité — stockés séparément en base
    formData.append('nom_declarant',     form.value.nom.trim().toUpperCase())
    formData.append('prenom_declarant',  form.value.prenom.trim())
    formData.append('date_naissance',    form.value.date_naissance)
    formData.append('lieu_naissance',    form.value.lieu_naissance.trim())
    formData.append('profession',        form.value.profession.trim())

    // Champs circonstances
    if (form.value.description) formData.append('description',  form.value.description.trim())
    if (form.value.lieu_perte)  formData.append('lieu_perte',   form.value.lieu_perte.trim())
    if (form.value.date_perte)  formData.append('date_perte',   form.value.date_perte)
    if (form.value.photo_piece) formData.append('photo_piece',  form.value.photo_piece)

    const { data } = await declarationsAPI.create(formData)
    createdDecl.value = data
    step.value = 4  // Écran de succès

  } catch (err) {
    const d = err.response?.data
    if (typeof d === 'object') {
      const keys = Object.keys(d)
      apiError.value = keys.length ? `${keys[0]} : ${d[keys[0]]}` : 'Une erreur est survenue.'
    } else {
      apiError.value = 'Erreur réseau. Vérifiez votre connexion.'
    }
    step.value = 3  // Rester sur recap
  } finally {
    submitting.value = false
  }
}

/* ══════════════════════════════════════
   TÉLÉCHARGEMENT PDF
══════════════════════════════════════ */
const downloadPDF = async () => {
  if (!createdDecl.value?.id) return
  try {
    const { data } = await declarationsAPI.downloadPDF(createdDecl.value.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${createdDecl.value.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    apiError.value = 'Impossible de générer le PDF pour le moment.'
  }
}

/* ══════════════════════════════════════
   HELPERS AFFICHAGE
══════════════════════════════════════ */
const selectedCategory = computed(() =>
  categories.value.find(c => c.id === form.value.categorie)
)
const typeLabel = computed(() =>
  form.value.type_declaration === 'PERTE' ? 'Perte' : 'Trouvaille'
)
const typeColor = computed(() =>
  form.value.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
)

const today = new Date().toISOString().split('T')[0]

// Icônes par catégorie (fallback)
const iconMap = {
  'id-card': '🪪', car: '🚗', 'graduation-cap': '🎓',
  'credit-card': '💳', briefcase: '💼', heart: '🏥', file: '📂',
}
const catIcon = (cat) => iconMap[cat.icone] || '📋'

const WIZARD_STEPS = [
  { num: 1, label: 'Type & catégorie' },
  { num: 2, label: 'Détails de la pièce' },
  { num: 3, label: 'Récapitulatif' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">

  <!-- ══════════════════════
       HEADER DE PAGE
  ══════════════════════ -->
  <div v-if="step < 4" class="max-w-2xl mx-auto mb-8">
    <router-link :to="{ name: 'home' }"
      class="inline-flex items-center gap-1.5 text-xs text-gray-400
             hover:text-[#005A3C] transition-colors no-underline mb-5">
      ← Retour à l'accueil
    </router-link>

    <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                text-xs font-bold px-3 py-1.5 rounded-full mb-3">
      📋 Nouvelle déclaration
    </div>
    <h1 class="font-serif text-[2rem] font-bold text-[#1A2E22] mb-1">
      Déclarer une perte ou trouvaille
    </h1>
    <p class="text-sm text-gray-500">
      Remplissez ce formulaire — un récépissé officiel PDF vous sera remis immédiatement.
    </p>
  </div>

  <!-- ══════════════════════
       STEPPER
  ══════════════════════ -->
  <div v-if="step < 4" class="max-w-2xl mx-auto mb-8">
    <div class="flex items-center">
      <template v-for="(s, i) in WIZARD_STEPS" :key="s.num">
        <div class="flex items-center gap-2">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300',
            step === s.num  ? 'bg-[#005A3C] text-white shadow-lg scale-110'
            : step > s.num  ? 'bg-[#005A3C]/20 text-[#005A3C]'
                            : 'bg-white text-gray-400 border border-gray-200'
          ]">
            <span v-if="step > s.num">✓</span>
            <span v-else>{{ s.num }}</span>
          </div>
          <span :class="[
            'text-xs font-medium hidden sm:block transition-colors',
            step === s.num ? 'text-[#1A2E22]' : 'text-gray-400'
          ]">{{ s.label }}</span>
        </div>

        <div v-if="i < WIZARD_STEPS.length - 1"
          :class="[
            'flex-1 h-px mx-3 transition-all duration-500',
            step > s.num ? 'bg-[#005A3C]' : 'bg-gray-200'
          ]">
        </div>
      </template>
    </div>

    <!-- Barre de progression -->
    <div class="mt-4 h-1 bg-gray-200 rounded-full overflow-hidden">
      <div class="h-full bg-[#005A3C] rounded-full transition-all duration-500"
        :style="{ width: `${((step - 1) / 2) * 100}%` }">
      </div>
    </div>
  </div>


  <!-- ════════════════════════════════════════
       ÉTAPE 1 — Type + Catégorie
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 1" key="s1" class="max-w-2xl mx-auto fade-up">
    <div class="card">

      <!-- Choix PERTE / TROUVAILLE -->
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1.5">
        Quel type de déclaration souhaitez-vous faire ?
      </h2>
      <p class="text-sm text-gray-500 mb-5">
        Choisissez selon votre situation.
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">

        <!-- PERTE -->
        <button type="button"
          @click="form.type_declaration = 'PERTE'"
          :class="[
            'relative rounded-xl p-6 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.type_declaration === 'PERTE'
              ? 'border-[#C41230] bg-red-50 shadow-lg'
              : 'border-gray-200 bg-white hover:border-red-200'
          ]">
          <!-- Indicateur sélectionné -->
          <div v-if="form.type_declaration === 'PERTE'"
            class="absolute top-3 right-3 w-5 h-5 bg-[#C41230] rounded-full
                   flex items-center justify-center text-white text-xs">✓</div>

          <div class="w-12 h-12 rounded-xl bg-red-100 flex items-center
                      justify-center text-2xl mb-4">😟</div>
          <div class="font-serif text-lg font-bold text-[#1A2E22] mb-1">
            J'ai perdu un document
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">
            Vous avez perdu une pièce administrative et souhaitez en faire la déclaration officielle.
          </p>
          <div class="mt-3 inline-block bg-[#C41230]/10 text-[#C41230]
                      text-xs font-bold px-2 py-1 rounded">PERTE</div>
        </button>

        <!-- TROUVAILLE -->
        <button type="button"
          @click="form.type_declaration = 'TROUVAILLE'"
          :class="[
            'relative rounded-xl p-6 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.type_declaration === 'TROUVAILLE'
              ? 'border-[#005A3C] bg-[#E8F4F0] shadow-lg'
              : 'border-gray-200 bg-white hover:border-green-200'
          ]">
          <div v-if="form.type_declaration === 'TROUVAILLE'"
            class="absolute top-3 right-3 w-5 h-5 bg-[#005A3C] rounded-full
                   flex items-center justify-center text-white text-xs">✓</div>

          <div class="w-12 h-12 rounded-xl bg-[#E8F4F0] flex items-center
                      justify-center text-2xl mb-4">🤲</div>
          <div class="font-serif text-lg font-bold text-[#1A2E22] mb-1">
            J'ai trouvé un document
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">
            Vous avez trouvé une pièce administrative et souhaitez aider son propriétaire à la récupérer.
          </p>
          <div class="mt-3 inline-block bg-[#005A3C]/10 text-[#005A3C]
                      text-xs font-bold px-2 py-1 rounded">TROUVAILLE</div>
        </button>
      </div>

      <!-- Catégorie -->
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1.5">
        Quelle est la catégorie du document ?
      </h2>
      <div class="flex items-center gap-2 mb-5">
        <p class="text-sm text-gray-500">Sélectionnez le type de pièce concernée.</p>
        <span v-if="!catsFromAPI && categories.length > 0"
          class="text-xs bg-yellow-100 text-yellow-700 font-medium px-2 py-0.5 rounded-full flex-shrink-0">
          ⚡ Mode hors ligne
        </span>
      </div>

      <div v-if="loadingCats" class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
        <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-xl"></div>
      </div>

      <!-- Grille catégories (erreur surlignée si oubliée) -->
      <div v-else
        :class="['grid grid-cols-2 sm:grid-cols-3 gap-3 mb-2', catError && !form.categorie && 'ring-2 ring-rouge/30 rounded-xl p-1']">
        <button type="button"
          v-for="cat in categories" :key="cat.id"
          @click="form.categorie = cat.id; catError = false"
          :class="[
            'rounded-xl p-4 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.categorie === cat.id
              ? 'border-[#005A3C] bg-[#E8F4F0] shadow-md'
              : catError && !form.categorie
                ? 'border-rouge/30 bg-white'
                : 'border-gray-200 bg-white hover:border-gray-300'
          ]">
          <span class="text-2xl block mb-2">{{ catIcon(cat) }}</span>
          <div :class="[
            'text-xs font-semibold leading-tight',
            form.categorie === cat.id ? 'text-[#005A3C]' : 'text-[#1A2E22]'
          ]">{{ cat.libelle }}</div>
        </button>
      </div>

      <!-- Message d'erreur catégorie -->
      <transition name="slide-error">
        <p v-if="catError && !form.categorie"
          class="flex items-center gap-1.5 text-xs text-rouge font-medium mb-4 mt-1">
          ⚠️ Veuillez sélectionner une catégorie pour continuer.
        </p>
        <div v-else class="mb-4"></div>
      </transition>

      <!-- Pied de carte -->
      <div class="flex items-center justify-between pt-4 border-t border-gray-100">
        <div class="text-xs text-gray-400">
          <span v-if="!form.type_declaration">← Choisissez un type</span>
          <span v-else-if="!form.categorie" class="text-[#D97706] font-medium">⬆ Choisissez aussi une catégorie</span>
          <span v-else class="text-[#005A3C] font-semibold">✓ Prêt à continuer</span>
        </div>
        <button type="button"
          @click="goNext"
          :disabled="!step1Valid"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-[10px] border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:-translate-y-0.5
                 disabled:opacity-40 disabled:cursor-not-allowed disabled:translate-y-0">
          Continuer →
        </button>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 2 — Détails de la pièce
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 2" key="s2" class="max-w-2xl mx-auto fade-up">
    <div class="card">

      <!-- Badge type sélectionné -->
      <div class="flex items-center gap-2 mb-6">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
          :style="{
            backgroundColor: form.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
            color: typeColor
          }">
          {{ form.type_declaration === 'PERTE' ? '😟' : '🤲' }} {{ typeLabel }}
        </div>
        <div class="flex items-center gap-1.5 bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full text-xs font-bold">
          {{ catIcon(selectedCategory || {}) }} {{ selectedCategory?.libelle }}
        </div>
        <button type="button" @click="goBack"
          class="ml-auto text-xs text-gray-400 hover:text-[#005A3C] bg-transparent
                 border-none cursor-pointer transition-colors">
          Modifier
        </button>
      </div>

      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-5">
        Informations sur la pièce
      </h2>

      <div class="space-y-5">

        <!-- Numéro de pièce (optionnel) -->
        <div>
          <label class="form-label">
            Numéro de la pièce
            <span class="text-gray-400 normal-case font-normal ml-1">(optionnel)</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔢</span>
            <input
              v-model="form.numero_piece"
              type="text"
              placeholder="Ex : TG20240001, AB-1234-CD"
              maxlength="100"
              class="form-input pl-10 uppercase"
              style="font-family: 'DM Mono', monospace, sans-serif; letter-spacing: 0.04em;"
            />
          </div>
          <p class="text-xs text-gray-400 mt-1.5">
            Si vous ne connaissez pas le numéro, laissez ce champ vide.
          </p>
        </div>

        <!-- Séparateur identité -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Identité sur la pièce</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Nom + Prénom séparés -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

          <!-- NOM DE FAMILLE -->
          <div>
            <label class="form-label">
              Nom de famille <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">👤</span>
              <input
                v-model="form.nom"
                type="text"
                placeholder="Ex : AKODJO"
                maxlength="100"
                class="form-input pl-10 uppercase"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Saisissez exactement comme indiqué sur votre pièce (majuscules incluses).
            </p>
          </div>

          <!-- PRÉNOM(S) -->
          <div>
            <label class="form-label">
              Prénom(s) <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✍️</span>
              <input
                v-model="form.prenom"
                type="text"
                placeholder="Ex : Jean Kofi"
                maxlength="100"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Saisissez exactement comme indiqué sur votre pièce.
            </p>
          </div>

        </div>

        <!-- Séparateur infos complémentaires -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Informations complémentaires</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Date de naissance + Lieu de naissance -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label">
              Date de naissance <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🎂</span>
              <input
                v-model="form.date_naissance"
                type="date"
                :max="today"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Telle qu'indiquée sur la pièce.
            </p>
          </div>
          <div>
            <label class="form-label">
              Lieu de naissance <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🏙️</span>
              <input
                v-model="form.lieu_naissance"
                type="text"
                placeholder="Ex : Lomé, Kpalimé, Sokodé"
                maxlength="100"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Tel qu'indiqué sur la pièce.
            </p>
          </div>
        </div>

        <!-- Profession -->
        <div>
          <label class="form-label">
            Profession <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">💼</span>
            <input
              v-model="form.profession"
              type="text"
              placeholder="Ex : Commerçant, Enseignant, Étudiant, Fonctionnaire"
              maxlength="100"
              class="form-input pl-10"
            />
          </div>
          <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
            <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
            Telle qu'indiquée sur votre pièce d'identité.
          </p>
        </div>

        <!-- Séparateur circonstances -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Circonstances</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Date + Lieu de la perte/trouvaille -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label">
              Date de la {{ form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille' }}
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">📅</span>
              <input
                v-model="form.date_perte"
                type="date"
                :max="today"
                class="form-input pl-10"
              />
            </div>
          </div>
          <div>
            <label class="form-label">
              Lieu de la {{ form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille' }}
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">📍</span>
              <input
                v-model="form.lieu_perte"
                type="text"
                placeholder="Ex : Marché de Lomé, Avenue de la Paix"
                maxlength="300"
                class="form-input pl-10"
              />
            </div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="form-label">
            Description <span class="text-gray-400 normal-case font-normal">(optionnel)</span>
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Décrivez les circonstances de la perte ou trouvaille, signes particuliers de la pièce…"
            maxlength="1000"
            class="form-input resize-none"
          ></textarea>
          <p class="text-xs text-gray-400 mt-1 text-right">
            {{ form.description.length }}/1000
          </p>
        </div>

        <!-- Upload Photo -->
        <div>
          <label class="form-label">
            Photo de la pièce <span class="text-gray-400 normal-case font-normal">(optionnel — max 5 MB)</span>
          </label>

          <!-- Aperçu photo -->
          <div v-if="photoPreview" class="relative mb-3 inline-block">
            <img :src="photoPreview" alt="Aperçu"
              class="h-28 w-auto rounded-xl object-cover border-2 border-[#005A3C]/30 shadow-md"/>
            <button type="button"
              @click="removePhoto"
              class="absolute -top-2 -right-2 w-6 h-6 bg-[#C41230] text-white rounded-full
                     flex items-center justify-center text-xs border-2 border-white cursor-pointer
                     shadow-md hover:bg-[#e8192f] transition-colors">✕</button>
          </div>

          <!-- Zone de drop -->
          <div v-if="!photoPreview"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer',
              isDragging
                ? 'border-[#005A3C] bg-[#E8F4F0]'
                : 'border-gray-200 bg-gray-50 hover:border-gray-300'
            ]"
            @click="$refs.photoInput.click()">
            <span class="text-3xl block mb-2">📷</span>
            <p class="text-sm text-gray-500 mb-1">Cliquez ou glissez une image</p>
            <p class="text-xs text-gray-400">JPG, PNG — max 5 MB</p>
          </div>
          <input ref="photoInput" type="file" accept="image/jpeg,image/jpg,image/png"
            class="hidden" @change="handlePhotoChange"/>
        </div>

      </div>

      <!-- Pied de carte -->
      <div class="flex items-center justify-between pt-6 mt-6 border-t border-gray-100">
        <button type="button" @click="goBack"
          class="flex items-center gap-2 text-sm font-medium text-gray-500 bg-white
                 border border-gray-200 px-5 py-3 rounded-[10px] cursor-pointer
                 hover:bg-gray-50 transition-all">
          ← Retour
        </button>
        <div class="flex items-center gap-3">
          <span v-if="!step2Valid" class="text-xs text-gray-400">
            Nom, prénom et informations d'identité requis
          </span>
          <button type="button"
            @click="goNext"
            :disabled="!step2Valid"
            class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                   text-sm px-6 py-3 rounded-[10px] border-none cursor-pointer
                   transition-all hover:bg-[#007A52] hover:-translate-y-0.5
                   disabled:opacity-40 disabled:cursor-not-allowed disabled:translate-y-0">
            Vérifier →
          </button>
        </div>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 3 — Récapitulatif + Confirmation
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 3" key="s3" class="max-w-2xl mx-auto fade-up">

    <!-- Erreur API -->
    <transition name="slide-error">
      <div v-if="apiError"
        class="flex items-start gap-3 bg-red-50 border border-red-200
               rounded-xl p-4 mb-5 text-sm text-rouge">
        <span class="text-lg leading-none mt-0.5">⚠️</span>
        <span>{{ apiError }}</span>
      </div>
    </transition>

    <div class="card">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-[#E8F4F0] rounded-full flex items-center justify-center text-lg">
          👁️
        </div>
        <div>
          <h2 class="font-serif text-lg font-bold text-[#1A2E22]">
            Vérifiez votre déclaration
          </h2>
          <p class="text-xs text-gray-500">Relisez avant de confirmer — aucune modification possible après soumission.</p>
        </div>
      </div>

      <!-- Bloc type -->
      <div class="rounded-xl p-4 mb-4 border-l-4"
        :style="{
          borderColor: typeColor,
          backgroundColor: form.type_declaration === 'PERTE' ? '#FEF2F2' : '#F0FDF4'
        }">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-lg">{{ form.type_declaration === 'PERTE' ? '😟' : '🤲' }}</span>
          <span class="font-bold text-sm" :style="{ color: typeColor }">
            Déclaration de {{ typeLabel.toUpperCase() }}
          </span>
        </div>
        <p class="text-xs text-gray-500">
          Catégorie : <strong>{{ selectedCategory?.libelle }}</strong>
        </p>
      </div>

      <!-- Tableau récap -->
      <div class="rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div v-for="(row, i) in [
          { label: 'Numéro de la pièce',  value: form.numero_piece.trim().toUpperCase() || 'Non communiqué', mono: true },
          { label: 'Nom de famille',       value: form.nom.trim().toUpperCase() },
          { label: 'Prénom(s)',            value: form.prenom.trim() },
          { label: 'Date de naissance',    value: form.date_naissance || '—' },
          { label: 'Lieu de naissance',    value: form.lieu_naissance || '—' },
          { label: 'Profession',           value: form.profession || '—' },
          { label: 'Date de la ' + (form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille'), value: form.date_perte || '—' },
          { label: 'Lieu',                 value: form.lieu_perte || '—' },
          { label: 'Description',          value: form.description || '—' },
          { label: 'Photo',                value: form.photo_piece ? form.photo_piece.name : 'Non fournie' },
        ]" :key="row.label"
          :class="[
            'flex items-start gap-3 px-4 py-3 text-sm',
            i % 2 === 0 ? 'bg-gray-50' : 'bg-white'
          ]">
          <span class="text-xs text-gray-500 font-medium w-36 flex-shrink-0 pt-0.5">
            {{ row.label }}
          </span>
          <span :class="['text-[#1A2E22] break-all', row.mono && 'font-mono font-bold tracking-wider text-[#005A3C]']">
            {{ row.value }}
          </span>
        </div>
      </div>

      <!-- Aperçu photo si dispo -->
      <div v-if="photoPreview" class="mb-6">
        <p class="text-xs text-gray-500 mb-2 font-medium">Aperçu de la photo jointe :</p>
        <img :src="photoPreview" alt="Photo de la pièce"
          class="h-24 w-auto rounded-xl object-cover border border-gray-200 shadow-sm"/>
      </div>

      <!-- Note légale -->
      <div class="bg-[#FFFBEB] border border-yellow-200 rounded-xl p-4 mb-6">
        <p class="text-xs text-yellow-700 leading-relaxed">
          ⚠️ <strong>Déclaration sur l'honneur.</strong> Toute fausse déclaration est punissable par la loi togolaise.
          En soumettant ce formulaire, vous certifiez l'exactitude des informations fournies.
        </p>
      </div>

      <!-- Boutons -->
      <div class="flex items-center justify-between">
        <button type="button" @click="goBack"
          :disabled="submitting"
          class="flex items-center gap-2 text-sm font-medium text-gray-500 bg-white
                 border border-gray-200 px-5 py-3 rounded-[10px] cursor-pointer
                 hover:bg-gray-50 transition-all disabled:opacity-50">
          ← Modifier
        </button>
        <button type="button"
          @click="handleSubmit"
          :disabled="submitting"
          class="flex items-center gap-2.5 font-bold text-sm px-8 py-3.5
                 rounded-[10px] border-none cursor-pointer transition-all
                 hover:-translate-y-0.5 hover:shadow-lg
                 disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0"
          :style="{
            backgroundColor: typeColor,
            color: 'white',
            boxShadow: submitting ? 'none' : `0 4px 16px ${typeColor}50`
          }">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>✅</span>
          <span>{{ submitting ? 'Envoi en cours...' : 'Confirmer la déclaration' }}</span>
        </button>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 4 — SUCCÈS 🎉
  ════════════════════════════════════════ -->
  <transition name="zoom-in" mode="out-in">
  <div v-if="step === 4" key="s4" class="max-w-xl mx-auto text-center py-4 fade-up">

    <!-- Cercle animé succès -->
    <div class="relative inline-flex items-center justify-center mb-6">
      <div class="w-24 h-24 rounded-full flex items-center justify-center text-4xl
                  shadow-xl"
        :style="{
          backgroundColor: form.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
        }">
        🎉
      </div>
      <!-- Cercle pulsant -->
      <div class="absolute inset-0 rounded-full animate-ping opacity-20"
        :style="{ backgroundColor: form.type_declaration === 'PERTE' ? '#C41230' : '#005A3C' }">
      </div>
    </div>

    <div class="inline-block bg-[#E8F4F0] text-[#005A3C] text-xs font-bold
                px-4 py-1.5 rounded-full mb-3">
      ✓ Déclaration enregistrée
    </div>

    <h2 class="font-serif text-[2rem] font-bold text-[#1A2E22] mb-3 leading-tight">
      Votre déclaration<br/>a bien été reçue !
    </h2>
    <p class="text-sm text-gray-500 max-w-sm mx-auto mb-6 leading-relaxed">
      Votre récépissé officiel est disponible. Vous serez notifié dès qu'une
      correspondance sera trouvée dans notre base de données.
    </p>

    <!-- Numéro de récépissé -->
    <div v-if="createdDecl" class="bg-white rounded-xl border-2 border-[#005A3C]/20
                                   p-5 mb-6 shadow-card">
      <p class="text-xs text-gray-500 mb-1">Numéro de récépissé</p>
      <div class="font-mono text-xl font-bold text-[#005A3C] tracking-wider">
        {{ createdDecl.numero_recepisse }}
      </div>
      <p class="text-xs text-gray-400 mt-2">
        Conservez ce numéro pour suivre votre déclaration.
      </p>
    </div>

    <!-- Erreur PDF -->
    <transition name="slide-error">
      <div v-if="apiError"
        class="flex items-start gap-3 bg-red-50 border border-red-200
               rounded-xl p-3 mb-4 text-sm text-rouge text-left">
        <span>⚠️</span><span>{{ apiError }}</span>
      </div>
    </transition>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <button type="button"
        @click="downloadPDF"
        class="inline-flex items-center justify-center gap-2.5 bg-[#005A3C] text-white
               font-bold px-6 py-3.5 rounded-[10px] border-none cursor-pointer
               transition-all hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg text-sm">
        📄 Télécharger mon récépissé PDF
      </button>

      <router-link :to="{ name: 'mes-declarations' }"
        class="inline-flex items-center justify-center gap-2.5 bg-white text-[#005A3C]
               font-semibold px-6 py-3.5 rounded-[10px] border border-[#005A3C]/30
               transition-all hover:bg-[#E8F4F0] hover:-translate-y-0.5 text-sm no-underline">
        📋 Voir mes déclarations
      </router-link>
    </div>

    <!-- Lien nouvelle déclaration -->
    <div class="mt-6">
      <button type="button"
        @click="() => { step = 1; form = { type_declaration: '', categorie: null, numero_piece: '', nom: '', prenom: '', date_naissance: '', lieu_naissance: '', profession: '', description: '', lieu_perte: '', date_perte: '', photo_piece: null }; photoPreview = null; createdDecl = null; apiError = null }"
        class="text-xs text-gray-400 hover:text-[#005A3C] bg-transparent
               border-none cursor-pointer transition-colors">
        + Faire une nouvelle déclaration
      </button>
    </div>

  </div>
  </transition>

</div>
</template>

<style scoped>
/* Transitions wizard */
.fade-step-enter-active,
.fade-step-leave-active { transition: all .3s ease; }
.fade-step-enter-from   { opacity: 0; transform: translateX(24px); }
.fade-step-leave-to     { opacity: 0; transform: translateX(-24px); }

/* Zoom succès */
.zoom-in-enter-active { transition: all .4s cubic-bezier(.175,.885,.32,1.275); }
.zoom-in-enter-from   { opacity: 0; transform: scale(.85); }

/* Erreur */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to { opacity: 0; transform: translateY(-8px); }

/* Spinner */
.loader-dot {
  display: inline-block;
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Input uppercase trick */
input.uppercase { text-transform: uppercase; }
input.uppercase::placeholder { text-transform: none; }
</style>