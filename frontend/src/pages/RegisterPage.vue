<template>
  <section class="section container">
    <div class="card form-card">
      <span class="badge">{{ t('register.badge') }}</span>
      <h3>{{ t('register.title') }}</h3>
      <p class="muted">{{ t('register.subtitle') }}</p>

      <form class="form-row" @submit.prevent="submitRegister">
        <div class="grid-2">
          <input v-model="firstName" class="input" type="text" :placeholder="t('register.firstName')" />
          <input v-model="lastName" class="input" type="text" :placeholder="t('register.lastName')" />
        </div>
        <input v-model="email" class="input" type="email" :placeholder="t('register.email')" />
        <input v-model="phone" class="input" type="tel" :placeholder="t('register.phone')" />
        <select v-model="role" class="input">
          <option value="customer">{{ t('register.roleCustomer') }}</option>
          <option value="admin">{{ t('register.roleAdmin') }}</option>
        </select>
        <input v-model="password" class="input" type="password" :placeholder="t('register.password')" />
        <button class="btn" type="submit" :disabled="loading">{{ loading ? t('register.loading') : t('register.button') }}</button>
        <p v-if="message" class="muted">{{ message }}</p>
        <p v-if="error" class="muted">{{ error }}</p>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../lib/api'
import { useLanguageStore } from '../stores/language'

const router = useRouter()
const language = useLanguageStore()
const t = language.t
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const role = ref('customer')
const password = ref('')
const loading = ref(false)
const error = ref('')
const message = ref('')

const submitRegister = async () => {
  loading.value = true
  error.value = ''
  message.value = ''
  try {
    await api.post('/auth/register', {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      phone: phone.value,
      role: role.value,
      password: password.value,
    })
    message.value = role.value === 'admin' ? t('register.successAdmin') : t('register.successCustomer')
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.detail || t('register.error')
  } finally {
    loading.value = false
  }
}
</script>
