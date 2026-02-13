<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { notificationsAPI } from '../../services/api'

const router = useRouter()

/* ══ État ══ */
const notifications = ref([])
const loading       = ref(true)
const markingAll    = ref(false)
const filterType    = ref('ALL')   // ALL | MATCH | STATUT | INFO | ADMIN

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await notificationsAPI.list()
    notifications.value = data.results ?? data
  } catch {}
  finally { loading.value = false }
})

/* ══ Filtrage ══ */
const filtered = computed(() => {
  if (filterType.value === 'ALL') return notifications.value
  return notifications.value.filter(n => n.type_notification === filterType.value)
})

const unreadCount = computed(() =>
  notifications.value.filter(n => !n.lue).length
)

/* ══ Actions ══ */
const markOne = async (notif) => {
  if (notif.lue) return
  try {
    await notificationsAPI.marquerLue(notif.id)
    notif.lue = true
  } catch {}
}

const markAll = async () => {
  if (!unreadCount.value) return
  markingAll.value = true
  try {
    await notificationsAPI.toutMarquer()
    notifications.value.forEach(n => { n.lue = true })
  } catch {}
  finally { markingAll.value = false }
}

/* ══ Naviguer vers la déclaration liée ══ */
const openNotif = (notif) => {
  markOne(notif)
  if (notif.declaration) {
    router.push({ name: 'declaration-detail', params: { id: notif.declaration } })
  }
}

/* ══ Helpers ══ */
const typeConfig = {
  MATCH:  { label: 'Correspondance', icon: '🎉', color: '#059669', bg: '#D1FAE5' },
  STATUT: { label: 'Statut',         icon: '📊', color: '#2563EB', bg: '#DBEAFE' },
  INFO:   { label: 'Information',    icon: 'ℹ️',  color: '#6B7280', bg: '#F3F4F6' },
  ADMIN:  { label: 'Administrateur', icon: '💬',  color: '#D97706', bg: '#FEF3C7' },
}
const getType = (t) => typeConfig[t] || typeConfig.INFO

const formatDate = (d) => {
  if (!d) return '—'
  const date = new Date(d)
  const now  = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60)   return 'À l\'instant'
  if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400)return `Il y a ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `Il y a ${Math.floor(diff / 86400)} j`
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

const typeFilters = [
  { key: 'ALL',   label: 'Toutes' },
  { key: 'MATCH', label: '🎉 Correspondances' },
  { key: 'STATUT',label: '📊 Statuts' },
  { key: 'INFO',  label: 'ℹ️ Infos' },
  { key: 'ADMIN', label: '💬 Admin' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-2xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🔔 Notifications
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] flex items-center gap-3">
        Mes notifications
        <span v-if="unreadCount > 0"
          class="text-sm font-bold bg-[#C41230] text-white px-2.5 py-0.5 rounded-full">
          {{ unreadCount }}
        </span>
      </h1>
    </div>
    <button v-if="unreadCount > 0"
      @click="markAll"
      :disabled="markingAll"
      class="flex items-center gap-2 text-xs font-semibold text-[#005A3C]
             bg-[#E8F4F0] border border-[#005A3C]/20 px-4 py-2.5 rounded-xl
             cursor-pointer hover:bg-[#d0ece3] transition-all disabled:opacity-50 border-none">
      <span v-if="markingAll" class="loader-dot-sm"></span>
      <span v-else">✓✓</span>
      Tout marquer comme lu
    </button>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex items-center gap-1 bg-white rounded-xl p-1 border border-gray-200
              shadow-sm mb-5 overflow-x-auto">
    <button v-for="f in typeFilters" :key="f.key"
      @click="filterType = f.key"
      :class="[
        'text-xs font-semibold px-3 py-2 rounded-lg whitespace-nowrap transition-all cursor-pointer border-none flex-shrink-0',
        filterType === f.key
          ? 'bg-[#005A3C] text-white shadow-sm'
          : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
      ]">
      {{ f.label }}
    </button>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 5" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="notifications.length === 0"
    class="text-center py-20 bg-white rounded-2xl shadow-card border border-gray-100">
    <div class="text-5xl mb-4">🔕</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">Aucune notification</p>
    <p class="text-sm text-gray-500">
      Vous serez notifié dès qu'une correspondance sera trouvée.
    </p>
  </div>

  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500">Aucune notification dans cette catégorie.</p>
    <button @click="filterType = 'ALL'"
      class="mt-2 text-xs text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      Voir toutes les notifications
    </button>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="notif in filtered" :key="notif.id"
        @click="openNotif(notif)"
        :class="[
          'rounded-2xl border transition-all cursor-pointer',
          'hover:-translate-y-0.5 hover:shadow-card-lg',
          notif.lue
            ? 'bg-white border-gray-100 shadow-sm'
            : 'bg-white border-[#005A3C]/20 shadow-card'
        ]">
        <div class="p-4 flex items-start gap-4">

          <!-- Icône type -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg
                      flex-shrink-0 relative"
            :style="{ backgroundColor: getType(notif.type_notification).bg }">
            {{ getType(notif.type_notification).icon }}
            <!-- Pastille non-lue -->
            <div v-if="!notif.lue"
              class="absolute -top-1 -right-1 w-3 h-3 bg-[#C41230] rounded-full
                     border-2 border-white">
            </div>
          </div>

          <!-- Contenu -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2">
              <p :class="['text-sm leading-snug', notif.lue ? 'text-gray-600' : 'font-semibold text-[#1A2E22]']">
                {{ notif.titre }}
              </p>
              <span class="text-xs text-gray-400 flex-shrink-0 mt-0.5">
                {{ formatDate(notif.date_creation) }}
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed line-clamp-2">
              {{ notif.message }}
            </p>

            <!-- Badge type + lien si déclaration liée -->
            <div class="flex items-center gap-2 mt-2">
              <span class="badge text-[10px]"
                :style="{
                  color: getType(notif.type_notification).color,
                  backgroundColor: getType(notif.type_notification).bg
                }">
                {{ getType(notif.type_notification).label }}
              </span>
              <span v-if="notif.declaration" class="text-[10px] text-gray-400">
                → Voir la déclaration
              </span>
              <span v-if="notif.lue" class="text-[10px] text-gray-300 ml-auto">Lu</span>
            </div>
          </div>

        </div>

        <!-- Barre colorée bas si non lue -->
        <div v-if="!notif.lue" class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getType(notif.type_notification).color, opacity: 0.35 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>
</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(8px); }
.line-clamp-2 {
  display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
}
.loader-dot-sm {
  display: inline-block; width: 12px; height: 12px;
  border: 2px solid rgba(0,90,60,.2); border-top-color: #005A3C;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>