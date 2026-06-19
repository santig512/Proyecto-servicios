<template>
  <section class="login-page section">
    <div class="login-shell container">
      <div class="login-card card">
        <div class="login-brand">
          <div class="login-title-row">
            <img class="login-logo" :src="logoImage" :alt="t('login.alt')" />
            <h3>{{ t('login.title') }}</h3>
          </div>
          <span class="badge">{{ t('common.access') }}</span>
          <p class="muted">{{ t('login.subtitle') }}</p>
        </div>

        <form class="form-row login-form" @submit.prevent="submitLogin">
          <input v-model="email" class="input" type="email" :placeholder="t('login.email')" />
          <input v-model="password" class="input" type="password" :placeholder="t('login.password')" />
          <button class="btn login-button" type="submit" :disabled="loading">{{ loading ? t('login.loading') : t('login.button') }}</button>
          <p v-if="error" class="muted login-error">{{ error }}</p>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../lib/api'
import { useAuthStore } from '../stores/auth'
import logoImage from '../assets/Logo TECH SOLUTIONS 1.png'
import { useLanguageStore } from '../stores/language'

const router = useRouter()
const auth = useAuthStore()
const language = useLanguageStore()
const t = language.t
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const submitLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.post('/auth/login', {
      email: email.value,
      password: password.value,
    })
    auth.setAuth(data.access_token, data.user)
    router.push(data.user?.role === 'admin' ? '/admin' : '/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || t('login.error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: auto;
  display: grid;
  align-items: center;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
}

.login-shell {
  width: 100%;
  display: grid;
  place-items: center;
}

.login-card {
  width: min(100%, 30rem);
  padding: 1.45rem;
  border-radius: 30px;
  background: #082756;
  color: #ffffff;
  box-shadow: 0 20px 50px rgba(8, 39, 86, 0.28);
}

.login-brand {
  display: grid;
  justify-items: start;
  gap: 0.7rem;
  margin-bottom: 1rem;
}

.login-title-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.login-logo {
  display: block;
  width: min(7.2rem, 24vw);
  height: auto;
}

.login-brand h3 {
  margin: 0;
  font-size: clamp(1.45rem, 2.4vw, 1.9rem);
  color: #ffffff;
}

.login-brand .muted {
  margin: 0;
  color: rgba(255, 255, 255, 0.82);
}

.login-form {
  margin-top: 0.35rem;
}

.login-form .input {
  border-radius: 18px;
  padding: 0.85rem 0.95rem;
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.login-form .input::placeholder {
  color: rgba(255, 255, 255, 0.72);
}

.login-button {
  width: 100%;
  border-radius: 18px;
  min-height: 2.9rem;
  color: #ffffff;
  background: linear-gradient(135deg, #f56e11, #ff8f3d);
}

.login-error {
  margin: 0.1rem 0 0;
  color: rgba(255, 255, 255, 0.82);
}

.login-card .badge {
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

@media (max-width: 640px) {
  .login-page {
    padding-top: 0.85rem;
    padding-bottom: 0.85rem;
  }

  .login-card {
    padding: 1.15rem;
    border-radius: 24px;
  }

  .login-title-row {
    align-items: flex-start;
  }
}
</style>
