<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()

const searchQuery    = ref('')
const searchCategory = ref('')

const handleSearch = () => {
  router.push({ name: 'search', query: {
    q:  searchQuery.value,
    cat: searchCategory.value,
  }})
}

const stats = [
  { num: '2 847', suffix: '+', key: 'declarations' },
  { num: '1 203', suffix: '+', key: 'found' },
  { num: '847',   suffix: '+', key: 'citizens' },
  { num: '42',    suffix: '%', key: 'rate' },
]

const features = [
  { icon: '🤝', key: 'matching' },
  { icon: '📄', key: 'pdf' },
  { icon: '🔔', key: 'notif' },
  { icon: '🔒', key: 'security' },
  { icon: '📱', key: 'mobile' },
  { icon: '🗂️', key: 'admin' },
]

const categories = [
  { icon: '🪪', key: 'identity', sub: 'CNI, Passeport' },
  { icon: '🚗', key: 'vehicle',  sub: 'Carte grise, Permis' },
  { icon: '🎓', key: 'school',   sub: 'Diplômes, Certificats' },
  { icon: '💳', key: 'bank',     sub: 'Cartes, Chéquiers' },
  { icon: '💼', key: 'pro',      sub: 'Badges, Cartes pro' },
  { icon: '🏥', key: 'health',   sub: 'Carnet, Assurance' },
  { icon: '📂', key: 'other',    sub: 'Tout document admin' },
]

const chips = ['CNI', 'Passeport', 'Carte grise', 'Permis', 'Diplôme']
</script>

<template>
  <section class="relative min-h-[92vh] grid grid-cols-1 md:grid-cols-2
                  items-center px-[5%] gap-12 overflow-hidden"
           style="background-color: var(--vert)">

    <div class="absolute inset-0 kente-bg opacity-30"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-transparent to-[#001a0e]/60"></div>

    <div class="relative z-10 py-20 fade-up">
      <div class="inline-block bg-[#D4A017]/20 text-[#D4A017] px-4 py-1.5 rounded-full border border-[#D4A017]/30 mb-7 text-sm font-bold">
        🇹🇬 {{ t('hero.badge') }}
      </div>
      
      <h1 class="font-serif text-[clamp(2.6rem,4.5vw,4rem)] font-bold
                 leading-[1.1] text-white mb-6">
        {{ t('hero.title1') }}<br/>
        <span class="text-[#D4A017] relative inline-block">
          {{ t('hero.title2') }}
          <span class="absolute bottom-1 left-0 right-0 h-[3px]
                       bg-[#D4A017] rounded-sm"></span>
        </span><br/>
        {{ t('hero.title3') }}
      </h1>
      
      <p class="text-white/90 text-lg leading-relaxed max-w-[500px] mb-10">
        {{ t('hero.subtitle') }}
      </p>
      
      <div class="flex gap-4 flex-wrap">
        <router-link :to="{ name: 'declare' }" class="btn-primary text-base px-7 py-3.5 no-underline">
          📋 {{ t('hero.cta_loss') }}
        </router-link>
        
        <router-link :to="{ name: 'search' }"
          class="inline-flex items-center gap-2 px-7 py-3.5 rounded-[10px]
                 bg-white/10 backdrop-blur text-white font-semibold text-base
                 border border-white/25 transition-all hover:bg-white/20
                 hover:-translate-y-0.5 no-underline">
          🔍 {{ t('hero.cta_search') }}
        </router-link>
      </div>
    </div>

    <div class="relative z-10 py-20 flex justify-end fade-up delay-200">
      <div class="bg-white/95 backdrop-blur-sm rounded-[20px] p-9 w-full max-w-[420px]
                  shadow-2xl">
        <h3 class="font-serif text-xl font-bold text-[#1A2E22] mb-1.5">
          {{ t('search.title') }}
        </h3>
        <p class="text-sm text-gray-500 mb-6 leading-relaxed">
          {{ t('search.subtitle') }}
        </p>

        <div class="relative mb-3">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input v-model="searchQuery" type="text"
            :placeholder="t('search.placeholder')"
            @keyup.enter="handleSearch"
            class="form-input pl-10"/>
        </div>

        <select v-model="searchCategory"
          class="form-input mb-4 cursor-pointer">
          <option value="">{{ t('search.all_cat') }}</option>
          <option value="1">{{ t('categories.identity') }}</option>
          <option value="2">{{ t('categories.vehicle') }}</option>
          <option value="3">{{ t('categories.school') }}</option>
          <option value="4">{{ t('categories.bank') }}</option>
          <option value="5">{{ t('categories.pro') }}</option>
          <option value="6">{{ t('categories.health') }}</option>
        </select>

        <button @click="handleSearch"
          class="w-full bg-[#005A3C] text-white font-bold py-3 rounded-[10px]
                 border-none cursor-pointer transition-all text-sm font-sans
                 hover:bg-[#007A52] hover:-translate-y-px flex items-center justify-center gap-2">
          🔍 {{ t('search.btn') }}
        </button>

        <div class="flex items-center gap-3 my-4">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400">{{ t('search.frequent') }}</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>
        <div class="flex gap-2 flex-wrap">
          <span v-for="chip in chips" :key="chip"
            @click="searchQuery = chip; handleSearch()"
            class="bg-[#E8F4F0] text-[#005A3C] text-xs font-semibold px-3 py-1.5
                   rounded-full cursor-pointer transition-all
                   hover:bg-[#005A3C] hover:text-white">
            {{ chip }}
          </span>
        </div>
      </div>
    </div>
  </section>

  <div class="bg-white border-t-4 border-[#D4A017] border-b border-gray-200
              px-[5%] py-8 grid grid-cols-2 md:grid-cols-4 gap-6">
    <div v-for="stat in stats" :key="stat.key" class="text-center">
      <div class="font-serif text-[2.2rem] font-bold text-[#005A3C] leading-none mb-1">
        {{ stat.num }}<span class="text-[#C41230] text-xl">{{ stat.suffix }}</span>
      </div>
      <div class="text-xs text-gray-500 font-medium">{{ t(`stats.${stat.key}`) }}</div>
    </div>
  </div>

  <section class="px-[5%] py-20" style="background-color: var(--creme)">
    <div class="text-xs font-bold tracking-widest text-[#005A3C] uppercase mb-2">📖 {{ t('steps.label') }}</div>
    <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
               text-[#1A2E22] leading-snug mb-4 max-w-xl">
      {{ t('steps.title') }}
    </h2>
    <p class="text-gray-500 leading-relaxed max-w-md mb-14">{{ t('steps.sub') }}</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
      <div class="hidden md:block absolute top-[28px] left-[calc(16.6%+28px)]
                  right-[calc(16.6%+28px)] h-0.5
                  bg-gradient-to-r from-[#005A3C] via-[#D4A017] to-[#005A3C]"></div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#005A3C]">
        <div class="w-14 h-14 bg-[#005A3C] text-white rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">1</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s1_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s1_text') }}</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#C41230]">
        <div class="w-14 h-14 bg-[#C41230] text-white rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">2</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s2_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s2_text') }}</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#D4A017]">
        <div class="w-14 h-14 bg-[#D4A017] text-[#005A3C] rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">3</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s3_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s3_text') }}</p>
      </div>
    </div>
  </section>

  <section class="px-[5%] py-20 relative overflow-hidden" 
           style="background-color: var(--vert)">
    
    <div class="absolute inset-0 kente-bg opacity-20"></div>

    <div class="relative z-10">
      <div class="inline-block bg-white/10 text-[#D4A017] border border-white/20 px-3 py-1 rounded text-xs font-bold mb-4">
        ✦ {{ t('features.label') }}
      </div>
      <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
                 text-white leading-snug mb-4 max-w-lg">
        {{ t('features.title') }}
      </h2>
      <p class="text-white/80 leading-relaxed max-w-md mb-12">{{ t('features.sub') }}</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
        <div v-for="f in features" :key="f.key"
          class="bg-white/10 border border-white/10 rounded-xl p-7 backdrop-blur-sm
                 transition-all hover:bg-white/20 hover:-translate-y-1">
          <span class="text-3xl block mb-4">{{ f.icon }}</span>
          <h3 class="font-serif text-base font-bold text-white mb-2">
            {{ t(`features.${f.key}`) }}
          </h3>
          <p class="text-sm text-white/80 leading-relaxed">
            {{ t(`features.${f.key}_txt`) }}
          </p>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-white px-[5%] py-20">
    <div class="text-xs font-bold tracking-widest text-[#005A3C] uppercase mb-2">📁 {{ t('categories.label') }}</div>
    <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
               text-[#1A2E22] leading-snug mb-10">
      {{ t('categories.title') }}
    </h2>
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="cat in categories" :key="cat.key"
        class="bg-white rounded-xl p-6 text-center shadow-md cursor-pointer
               transition-all hover:border-[#005A3C] hover:-translate-y-1 hover:shadow-xl
               border-2 border-transparent"
        @click="router.push({ name: 'search', query: { cat: cat.key }})">
        <span class="text-3xl block mb-3">{{ cat.icon }}</span>
        <div class="text-sm font-semibold text-[#1A2E22] mb-1">{{ t(`categories.${cat.key}`) }}</div>
        <div class="text-xs text-gray-400">{{ cat.sub }}</div>
      </div>

      <div class="rounded-xl p-6 text-center border-2 border-dashed border-gray-200
                  bg-gray-50 cursor-default flex flex-col items-center justify-center">
        <span class="text-3xl block mb-3">➕</span>
        <div class="text-sm font-semibold text-gray-400 mb-1">{{ t('categories.suggest') }}</div>
        <div class="text-xs text-gray-300">Contactez-nous</div>
      </div>
    </div>
  </section>

  <section class="relative overflow-hidden px-[5%] py-20 text-center
                  bg-gradient-to-br from-[#C41230] to-[#8B0D22]">
    <div class="absolute inset-0"
      style="background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.04) 0 1px,transparent 1px 20px)">
    </div>
    <h2 class="font-serif text-[clamp(2rem,3.5vw,3rem)] font-bold
               text-white mb-4 relative z-10">
      {{ t('cta.title') }}
    </h2>
    <p class="text-white/80 max-w-lg mx-auto mb-9 leading-relaxed relative z-10">
      {{ t('cta.sub') }}
    </p>
    <div class="flex gap-4 justify-center flex-wrap relative z-10">
      <router-link :to="{ name: 'declare' }"
        class="bg-white text-[#C41230] font-bold px-8 py-3.5 rounded-[10px]
               no-underline inline-flex items-center gap-2 transition-all
               hover:-translate-y-0.5 hover:shadow-xl">
        📋 {{ t('cta.loss') }}
      </router-link>
      <router-link :to="{ name: 'declare', query: { type: 'TROUVAILLE' }}"
        class="bg-transparent text-white font-semibold px-8 py-3.5 rounded-[10px]
               border-2 border-white/40 no-underline inline-flex items-center gap-2
               transition-all hover:border-white hover:bg-white/10 hover:-translate-y-0.5">
        📦 {{ t('cta.found') }}
      </router-link>
    </div>
  </section>

  <footer class="bg-[#1A2E22] px-[5%] pt-14 pb-6 text-white/60">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
      <div class="md:col-span-2">
        <div class="font-serif text-xl font-bold text-white mb-3">
          Décla<span class="text-[#D4A017]">Togo</span>
        </div>
        <p class="text-sm leading-relaxed max-w-xs">{{ t('footer.desc') }}</p>
        <div class="flex mt-4 h-1.5 w-20 rounded overflow-hidden">
          <div class="flex-[2] bg-[#005A3C]"></div>
          <div class="flex-1 bg-[#FFCE00]"></div>
          <div class="flex-[2] bg-[#C41230]"></div>
        </div>
      </div>
      <div>
        <div class="text-xs font-bold uppercase tracking-widest text-white mb-4">
          {{ t('footer.services') }}
        </div>
        <ul class="space-y-2.5 pl-0">
          <li class="list-none"><router-link :to="{ name: 'declare' }"
            class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('hero.cta_loss') }}
          </router-link></li>
          <li class="list-none"><router-link :to="{ name: 'search' }"
            class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('nav.search') }}
          </router-link></li>
        </ul>
      </div>
      <div>
        <div class="text-xs font-bold uppercase tracking-widest text-white mb-4">
          {{ t('footer.info') }}
        </div>
        <ul class="space-y-2.5 pl-0">
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">FAQ</a></li>
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">Contact</a></li>
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('footer.legal') }}
          </a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-white/10 pt-6 flex flex-col md:flex-row
                items-center justify-between gap-3 text-xs">
      <span>{{ t('footer.rights') }}</span>
      <span>{{ t('footer.made') }} ❤️</span>
    </div>
  </footer>
</template>