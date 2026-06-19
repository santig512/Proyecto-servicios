<template>
  <div class="chat-widget card" v-if="visible">
    <div class="chat-header">
      <strong>Chat</strong>
      <button class="btn secondary" @click="visible=false">Cerrar</button>
    </div>
    <div class="chat-body">
      <div v-for="m in messages" :key="m.id" class="chat-msg">{{ m }}</div>
    </div>
    <form @submit.prevent="sendMessage" class="form-row">
      <input v-model="text" class="input" placeholder="Escribe un mensaje" />
      <button class="btn" :disabled="!connected">Enviar</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const visible = ref(true)
const messages = ref([])
const text = ref('')
let socket = null
const connected = ref(false)

function connect() {
  if (!auth.token) return
  socket = new WebSocket(`${location.origin.replace('http', 'ws')}/api/v1/chat/ws/general?token=${auth.token}`)
  socket.addEventListener('open', () => { connected.value = true })
  socket.addEventListener('message', (ev) => { messages.value.push(ev.data) })
  socket.addEventListener('close', () => { connected.value = false })
}

function sendMessage() {
  if (!socket || socket.readyState !== WebSocket.OPEN) return
  socket.send(text.value)
  text.value = ''
}

onMounted(() => {
  connect()
})

onBeforeUnmount(() => {
  if (socket) socket.close()
})
</script>

<style scoped>
.chat-widget { width: 320px; position: fixed; right: 1rem; bottom: 1rem; padding: 0.75rem; }
.chat-body { max-height: 240px; overflow: auto; margin-bottom: 0.5rem; }
.chat-msg { padding: 0.35rem 0.4rem; border-bottom: 1px solid rgba(255,255,255,0.03); }
.chat-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem }
</style>
