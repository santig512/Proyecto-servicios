<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <RouterLink class="brand-mark brand-mark-link" to="/" aria-label="Ir al inicio">
          <img class="brand-logo-image" :src="techSolutionsLogo" alt="24HR Tech Solutions" />
        </RouterLink>
      </div>
      <div class="nav-panel">
        <div class="language-switcher" aria-label="Language switcher">
          <button
            type="button"
            class="lang-button"
            :class="{ active: locale === 'es' }"
            @click="setLocale('es')"
          >
            {{ t('language.spanish') }}
          </button>
          <button
            type="button"
            class="lang-button"
            :class="{ active: locale === 'en' }"
            @click="setLocale('en')"
          >
            {{ t('language.english') }}
          </button>
        </div>
        <nav v-if="!isAuthenticated" class="nav-links">
          <RouterLink to="/">{{ t('nav.home') }}</RouterLink>
          <RouterLink to="/login">{{ t('nav.login') }}</RouterLink>
        </nav>
        <div v-if="!isAuthenticated" class="nav-cta-wrap">
          <RouterLink class="nav-cta" to="/services">{{ t('nav.service') }}</RouterLink>
        </div>
        <div v-if="isAuthenticated" class="auth-actions">
          <button class="btn secondary" type="button" @click="handleLogout">{{ t('nav.logout') }}</button>
        </div>
      </div>
    </header>

    <main class="page-shell">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import Swal from 'sweetalert2'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import techSolutionsLogo from './assets/Logo TECH SOLUTIONS 2.png'
import { useLanguageStore } from './stores/language'

const auth = useAuthStore()
const router = useRouter()
const isAuthenticated = computed(() => !!auth.token)
const language = useLanguageStore()
const { locale } = storeToRefs(language)
const t = language.t

const handleLogout = async () => {
  const result = await Swal.fire({
    title: t('logout.title'),
    text: t('logout.text'),
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: t('common.confirmLogout'),
    cancelButtonText: t('common.cancel'),
  })

  if (!result.isConfirmed) return

  auth.clearAuth()
  await router.push('/login')
}

const setLocale = (selectedLocale) => {
  language.setLocale(selectedLocale)
}
</script>
