<template>
  <section class="section container">
    <div class="grid-3">
      <div class="card metric">
        <strong>64</strong>
        <span class="muted">{{ t('adminDashboard.assigned') }}</span>
      </div>
      <div class="card metric">
        <strong>18</strong>
        <span class="muted">{{ t('adminDashboard.pendingQuotes') }}</span>
      </div>
      <div class="card metric">
        <strong>9</strong>
        <span class="muted">{{ t('adminDashboard.invoices') }}</span>
      </div>
    </div>

    <div class="grid-2" style="margin-top: 1rem;">
      <div class="card" style="padding: 1.25rem;">
        <h3>{{ t('adminDashboard.commercialFlow') }}</h3>
        <p class="muted">{{ t('adminDashboard.commercialText') }}</p>
      </div>
      <div class="card" style="padding: 1.25rem;">
        <h3>{{ t('adminDashboard.operation') }}</h3>
        <p class="muted">{{ t('adminDashboard.operationText') }}</p>
      </div>
    </div>

    <div class="card" style="margin-top: 1rem; padding: 1.25rem; display:flex; justify-content:space-between; gap:1rem; align-items:center; flex-wrap:wrap;">
      <div>
        <h3 style="margin:0;">{{ t('adminDashboard.userManagement') }}</h3>
        <p class="muted" style="margin:0.25rem 0 0;">{{ t('adminDashboard.userManagementText') }}</p>
      </div>
      <RouterLink class="btn" to="/admin/users">{{ t('adminDashboard.openUsers') }}</RouterLink>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useLanguageStore } from '../stores/language'

const language = useLanguageStore()
const t = language.t
</script>
