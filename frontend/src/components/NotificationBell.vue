<template>
  <div class="notification-bell">
    <button class="btn" @click="toggle">
      🔔 <span v-if="unreadCount">({{ unreadCount }})</span>
    </button>
    <div class="dropdown card" v-if="open">
      <div v-if="loading" class="muted">{{ t('notifications.loading') }}</div>
      <div v-if="!loading && notifications.length===0" class="muted">{{ t('notifications.empty') }}</div>
      <ul>
        <li v-for="n in notifications" :key="n.id">
          <strong>{{ n.title }}</strong>
          <div class="muted">{{ n.body }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../lib/api'
import { useAuthStore } from '../stores/auth'
import { useLanguageStore } from '../stores/language'

const auth = useAuthStore()
const language = useLanguageStore()
const t = language.t
const open = ref(false)
const notifications = ref([])
const loading = ref(false)
const unreadCount = ref(0)

const load = async () => {
  if (!auth.token) return
  loading.value = true
  try {
    const { data } = await api.get('/notifications')
    notifications.value = data
    unreadCount.value = data.filter(n => !n.is_read).length
  } catch (err) {
    notifications.value = []
  } finally {
    loading.value = false
  }
}

const toggle = () => {
  open.value = !open.value
  if (open.value) load()
}

onMounted(load)
</script>

<style scoped>
.notification-bell { position: relative }
.dropdown { position: absolute; right: 0; top: 2.4rem; width: 320px; padding: 0.6rem }
.dropdown ul { list-style: none; padding: 0; margin: 0 }
.dropdown li { padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.03) }
</style>
