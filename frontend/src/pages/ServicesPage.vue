<template>
  <section class="services-page section">
    <div class="services-shell container">
      <div class="services-card card">
        <div class="services-brand">
          <div class="services-title-row">
            <img class="services-logo" :src="logoImage" :alt="t('services.alt')" />
            <h3>{{ t('services.title') }}</h3>
          </div>
          <span class="badge">{{ t('common.publicRequest') }}</span>
          <p class="muted">{{ t('services.subtitle') }}</p>
        </div>

        <div class="services-layout">
          <form class="form-row services-form" @submit.prevent="submitRequest">
            <div class="grid-2 services-grid">
              <input v-model="customerName" class="input" type="text" :placeholder="t('services.name')" />
              <input v-model="customerPhone" class="input" type="tel" :placeholder="t('services.phone')" />
            </div>
            <div class="grid-2 services-grid">
              <input v-model="customerEmail" class="input" type="email" :placeholder="t('services.email')" />
              <input v-model="serviceAddress" class="input" type="text" :placeholder="t('services.address')" />
            </div>
            <div class="grid-2 services-grid">
              <input v-model="postalCode" class="input" type="text" :placeholder="t('services.postalCode')" />
              <input v-model="title" class="input" type="text" :placeholder="t('services.type')" />
            </div>
            <input v-model="scheduledDate" class="input" type="datetime-local" :aria-label="t('services.date')" />
            <textarea v-model="description" class="input" rows="3" :placeholder="t('services.description')"></textarea>
            <button class="btn services-button" type="submit" :disabled="saving">{{ saving ? t('services.submitting') : t('services.submit') }}</button>
            <p v-if="saveMessage" class="muted services-message">{{ saveMessage }}</p>
            <p v-if="saveError" class="muted services-message">{{ saveError }}</p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../lib/api'
import logoImage from '../assets/Logo TECH SOLUTIONS 1.png'
import { useLanguageStore } from '../stores/language'

const language = useLanguageStore()
const t = language.t
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref('')
const customerName = ref('')
const customerPhone = ref('')
const customerEmail = ref('')
const serviceAddress = ref('')
const postalCode = ref('')
const title = ref('')
const description = ref('')
const scheduledDate = ref('')

const submitRequest = async () => {
  saving.value = true
  saveMessage.value = ''
  saveError.value = ''
  try {
    const { data } = await api.post('/services/public', {
      customer_name: customerName.value,
      customer_phone: customerPhone.value,
      customer_email: customerEmail.value,
      service_address: serviceAddress.value,
      postal_code: postalCode.value,
      title: title.value,
      description: description.value,
      scheduled_date: scheduledDate.value || null,
    })
    saveMessage.value = `${t('services.success')} ${data.tracking_code}.`
  } catch (err) {
    saveError.value = err.response?.data?.detail || t('services.saveError')
  } finally {
    saving.value = false
  }
}

onMounted(() => {})
</script>

<style scoped>
.services-page {
  min-height: auto;
  display: grid;
  align-items: center;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.services-shell {
  width: 100%;
  display: grid;
  place-items: center;
}

.services-card {
  width: min(100%, 48rem);
  padding: 0.9rem;
  border-radius: 22px;
  background: #082756;
  color: #ffffff;
  box-shadow: 0 14px 30px rgba(8, 39, 86, 0.22);
}

.services-brand {
  display: grid;
  justify-items: start;
  gap: 0.35rem;
  margin-bottom: 0.55rem;
}

.services-title-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.services-logo {
  display: block;
  width: min(5.6rem, 20vw);
  height: auto;
}

.services-brand h3,
.services-track-header h4 {
  margin: 0;
  color: #ffffff;
}

.services-brand h3 {
  font-size: clamp(1.1rem, 1.9vw, 1.45rem);
}

.services-brand .muted,
.services-message,
.services-track-header .muted {
  margin: 0;
  color: rgba(255, 255, 255, 0.82);
}

.services-form {
  margin-top: 0.1rem;
}

.services-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  align-items: start;
}

.services-grid {
  gap: 0.45rem;
}

.services-form .input,
.services-form .input {
  padding: 0.65rem 0.8rem;
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.services-form .input::placeholder {
  color: rgba(255, 255, 255, 0.72);
}

.services-form .input[type="datetime-local"] {
  color-scheme: dark;
}

.services-form textarea.input {
  min-height: 4rem;
  resize: vertical;
}

.services-button {
  width: 100%;
  border-radius: 18px;
  min-height: 2.45rem;
  color: #ffffff;
  background: linear-gradient(135deg, #f56e11, #ff8f3d);
}

@media (max-width: 640px) {
  .services-page {
    padding-top: 0.45rem;
    padding-bottom: 0.45rem;
  }

  .services-card {
    padding: 0.85rem;
    border-radius: 18px;
  }

  .services-title-row {
    align-items: flex-start;
  }

  .services-form .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
