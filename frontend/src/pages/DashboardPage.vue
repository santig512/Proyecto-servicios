<template>
  <section class="section container">
    <div class="grid-3">
      <div class="card metric">
        <strong>{{ stats.total }}</strong>
        <span class="muted">{{ t('dashboard.servicesLoaded') }}</span>
      </div>
      <div class="card metric">
        <strong>{{ stats.pending }}</strong>
        <span class="muted">{{ t('dashboard.pending') }}</span>
      </div>
      <div class="card metric">
        <strong>{{ stats.inProgress }}</strong>
        <span class="muted">{{ t('dashboard.inProgress') }}</span>
      </div>
    </div>

    <div class="card" style="margin-top: 1rem; padding: 1.25rem; overflow: auto;">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
        <div>
          <h3>{{ t('dashboard.title') }}</h3>
          <p class="muted">{{ t('dashboard.subtitle') }}</p>
        </div>
        <button class="btn secondary" type="button" @click="loadServices" :disabled="loading">
          {{ loading ? t('dashboard.refreshing') : t('dashboard.refresh') }}
        </button>
      </div>

      <p v-if="error" class="muted" style="margin-top: 0.75rem;">{{ error }}</p>
      <p v-if="saveMessage" class="muted" style="margin-top: 0.75rem;">{{ saveMessage }}</p>

      <table v-if="services.length" class="table" style="margin-top: 1rem;">
        <thead>
          <tr>
            <th>{{ t('dashboard.service') }}</th>
            <th>{{ t('dashboard.client') }}</th>
            <th>{{ t('dashboard.postalCode') }}</th>
            <th>{{ t('dashboard.code') }}</th>
            <th>{{ t('dashboard.status') }}</th>
            <th>{{ t('dashboard.priority') }}</th>
            <th>{{ t('dashboard.date') }}</th>
            <th>{{ t('dashboard.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>
              <strong>{{ service.title }}</strong>
              <div class="muted">{{ service.service_address || t('dashboard.noAddress') }}</div>
            </td>
            <td>
              <div>{{ service.customer_name || t('dashboard.noName') }}</div>
              <div class="muted">{{ service.customer_email || t('dashboard.noEmail') }}</div>
            </td>
            <td>{{ service.postal_code || t('dashboard.noPostalCode') }}</td>
            <td>{{ service.tracking_code }}</td>
            <td>
              <select v-model="service.status" class="input select-dark" style="min-width: 140px;">
                <option value="pending">{{ t('dashboard.statuses.pending') }}</option>
                <option value="assigned">{{ t('dashboard.statuses.assigned') }}</option>
                <option value="in_progress">{{ t('dashboard.statuses.inProgress') }}</option>
                <option value="completed">{{ t('dashboard.statuses.completed') }}</option>
                <option value="cancelled">{{ t('dashboard.statuses.cancelled') }}</option>
              </select>
            </td>
            <td>
              <select v-model="service.priority" class="input select-dark" style="min-width: 120px;">
                <option value="low">{{ t('dashboard.priorities.low') }}</option>
                <option value="normal">{{ t('dashboard.priorities.normal') }}</option>
                <option value="medium">{{ t('dashboard.priorities.medium') }}</option>
                <option value="high">{{ t('dashboard.priorities.high') }}</option>
              </select>
            </td>
            <td>{{ formatDate(service.scheduled_date) }}</td>
            <td>
              <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <button class="btn secondary" type="button" :disabled="savingId === service.id" @click="saveService(service)">
                  {{ savingId === service.id ? t('dashboard.saving') : t('dashboard.save') }}
                </button>
                <button class="btn secondary" type="button" :disabled="savingId === service.id" @click="deleteService(service)">
                  {{ t('common.delete') }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else-if="!loading" class="muted" style="margin-top: 1rem;">
        {{ t('dashboard.empty') }}
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api } from '../lib/api'
import Swal from 'sweetalert2'
import { useLanguageStore } from '../stores/language'

const auth = useAuthStore()
const language = useLanguageStore()
const t = language.t
const services = ref([])
const loading = ref(false)
const error = ref('')
const saveMessage = ref('')
const savingId = ref(null)
const canManage = computed(() => auth.user?.role === 'admin' || auth.user?.role === 'technician')

const stats = computed(() => ({
  total: services.value.length,
  pending: services.value.filter((service) => service.status === 'pending').length,
  inProgress: services.value.filter((service) => service.status === 'assigned' || service.status === 'in_progress').length,
}))

const loadServices = async () => {
  loading.value = true
  error.value = ''
  saveMessage.value = ''
  try {
    const { data } = await api.get('/services/me')
    services.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || t('dashboard.errorLoad')
  } finally {
    loading.value = false
  }
}

const saveService = async (service) => {
  if (!canManage.value) {
    error.value = t('dashboard.noManage')
    return
  }
  savingId.value = service.id
  error.value = ''
  saveMessage.value = ''
  try {
    const { data } = await api.patch(`/services/${service.id}`, {
      status: service.status,
      priority: service.priority,
    })
    Object.assign(service, data)
    saveMessage.value = `${t('dashboard.updatedMessage')} ${service.tracking_code}.`
  } catch (err) {
    error.value = err.response?.data?.detail || t('dashboard.errorUpdate')
  } finally {
    savingId.value = null
  }
}

const deleteService = async (service) => {
  if (!canManage.value) {
    error.value = t('dashboard.noDelete')
    return
  }

  const result = await Swal.fire({
    title: t('dashboard.deleteTitle'),
    text: `${t('dashboard.deletePrompt')} ${service.tracking_code}?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: t('dashboard.deleteConfirm'),
    cancelButtonText: t('dashboard.deleteCancel'),
    confirmButtonColor: '#d33',
  })

  if (!result.isConfirmed) return

  savingId.value = service.id
  error.value = ''
  saveMessage.value = ''

  try {
    await api.delete(`/services/${service.id}`)
    services.value = services.value.filter((item) => item.id !== service.id)
    saveMessage.value = `${t('dashboard.deleteSuccess')} ${service.tracking_code}.`
    await Swal.fire({
      title: t('dashboard.deleteDoneTitle'),
      text: t('dashboard.deleteDoneText'),
      icon: 'success',
      confirmButtonText: t('dashboard.deleteOk'),
    })
  } catch (err) {
    error.value = err.response?.data?.detail || t('dashboard.deleteError')
    await Swal.fire({
      title: t('dashboard.deleteErrorTitle'),
      text: error.value,
      icon: 'error',
      confirmButtonText: t('dashboard.deleteOk'),
    })
  } finally {
    savingId.value = null
  }
}

const formatDate = (value) => {
  if (!value) return t('dashboard.noDate')
  return new Date(value).toLocaleString(language.locale === 'en' ? 'en-US' : 'es-ES', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

onMounted(loadServices)
</script>
