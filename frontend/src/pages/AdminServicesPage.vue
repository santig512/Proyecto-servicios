<template>
  <section class="section container">
    <div class="card" style="padding: 1.25rem;">
      <h3>{{ t('adminServices.title') }}</h3>
      <p v-if="loading" class="muted">{{ t('adminServices.loading') }}</p>
      <p v-if="error" class="muted">{{ error }}</p>
      <table class="table" v-if="services.length">
        <thead>
          <tr>
            <th>{{ t('adminServices.headerService') }}</th>
            <th>{{ t('adminServices.headerContact') }}</th>
            <th>{{ t('adminServices.headerStatus') }}</th>
            <th>{{ t('adminServices.headerCode') }}</th>
            <th>{{ t('adminServices.headerActions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.title }}</td>
            <td>
              <div>{{ service.customer_name || t('adminServices.noName') }}</div>
              <div class="muted">{{ service.customer_email || t('adminServices.noEmail') }}</div>
              <div class="muted">{{ service.customer_phone || t('adminServices.noPhone') }}</div>
            </td>
            <td><span class="badge">{{ statusLabel(service.status) }}</span></td>
            <td>{{ service.tracking_code }}</td>
            <td>
              <button class="btn secondary" @click="editService(service)">{{ t('adminServices.viewEdit') }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../lib/api'
import Swal from 'sweetalert2'
import { useLanguageStore } from '../stores/language'

const language = useLanguageStore()
const t = language.t
const services = ref([])
const loading = ref(false)
const error = ref('')

const loadServices = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/services')
    services.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || t('adminServices.errorLoad')
  } finally {
    loading.value = false
  }
}

const editService = (service) => {
  Swal.fire({
    title: t('adminServices.editTitle'),
    text: `${t('adminServices.editText')} ${service.tracking_code}`,
    icon: 'info',
    confirmButtonText: t('adminServices.editOk'),
  })
}

const statusLabel = (status) => {
  const normalizedStatus = status === 'in_progress' ? 'inProgress' : status
  return t(`adminServices.statuses.${normalizedStatus}`)
}

onMounted(loadServices)
</script>
