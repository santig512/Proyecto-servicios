import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles.css'
import NotificationBell from './components/NotificationBell.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('NotificationBell', NotificationBell)
app.mount('#app')
