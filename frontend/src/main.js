import { createApp } from 'vue'
import { createPinia } from 'pinia' // ← ДОБАВИТЬ
import App from './App.vue'
import router from './router'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

const app = createApp(App)
app.use(createPinia()) // ← ДОБАВИТЬ
app.use(router)
app.mount('#app')
