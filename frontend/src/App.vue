<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <RouterLink class="brand-mark brand-mark-link" to="/" aria-label="Ir al inicio">
          <img class="brand-logo-image" :src="techSolutionsLogo" alt="24HR Tech Solutions" />
        </RouterLink>
      </div>
      <div class="nav-panel">
        <div class="language-switcher desktop-only" aria-label="Language switcher">
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
        <nav v-if="!isAuthenticated" class="nav-links desktop-only">
          <RouterLink to="/">{{ t('nav.home') }}</RouterLink>
          <RouterLink to="/login">{{ t('nav.login') }}</RouterLink>
        </nav>
        <div v-if="!isAuthenticated" class="nav-cta-wrap desktop-only">
          <RouterLink class="nav-cta" to="/services">{{ t('nav.service') }}</RouterLink>
        </div>
        <div v-if="isAuthenticated" class="auth-actions desktop-only">
          <button class="btn secondary" type="button" @click="handleLogout">{{ t('nav.logout') }}</button>
        </div>
        <button
          type="button"
          class="menu-toggle mobile-only"
          :class="{ open: menuOpen }"
          :aria-expanded="menuOpen"
          :aria-label="menuOpen ? t('common.cancel') : 'Abrir menú'"
          @click="toggleMenu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      <transition name="mobile-menu-fade">
        <div v-if="menuOpen" class="mobile-menu mobile-only" @click.self="closeMenu">
          <div class="mobile-menu-panel card">
            <div class="language-switcher mobile-menu-language" aria-label="Language switcher">
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

            <nav v-if="!isAuthenticated" class="mobile-nav-links">
              <RouterLink to="/" @click="closeMenu">{{ t('nav.home') }}</RouterLink>
              <RouterLink to="/login" @click="closeMenu">{{ t('nav.login') }}</RouterLink>
              <RouterLink class="mobile-nav-cta" to="/services" @click="closeMenu">{{ t('nav.service') }}</RouterLink>
            </nav>

            <div v-if="isAuthenticated" class="mobile-auth-actions">
              <button class="btn secondary" type="button" @click="handleLogout">{{ t('nav.logout') }}</button>
            </div>
          </div>
        </div>
      </transition>
    </header>

    <main class="page-shell">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { computed, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import Swal from 'sweetalert2'
import { useAuthStore } from './stores/auth'
import { useRouter, useRoute } from 'vue-router'
import techSolutionsLogo from './assets/Logo TECH SOLUTIONS 2.png'
import { useLanguageStore } from './stores/language'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const isAuthenticated = computed(() => !!auth.token)
const language = useLanguageStore()
const { locale } = storeToRefs(language)
const t = language.t
const menuOpen = ref(false)

const closeMenu = () => {
  menuOpen.value = false
}

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

watch(() => route.fullPath, () => {
  closeMenu()
})

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
  closeMenu()
  await router.push('/login')
}

const setLocale = (selectedLocale) => {
  language.setLocale(selectedLocale)
}
</script>
