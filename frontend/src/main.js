import { createApp }  from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios' // 1. On importe axios

import App          from './App.vue'
import router       from './router'
import i18n         from './i18n'
import './style.css' // 2. On garde précieusement ton CSS !

// 3. Configuration de l'URL de base pour Django
// Cela évitera l'erreur 404 car tous tes appels seront préfixés par /api/
axios.defaults.baseURL = 'http://localhost:8000/api/'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')