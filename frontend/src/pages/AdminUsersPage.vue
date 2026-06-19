<template>
  <section class="section container">
    <div class="card" style="padding: 1.25rem;">
      <h3>{{ t('adminUsers.title') }}</h3>
      <form class="form-row" style="margin: 1rem 0 1.5rem;" @submit.prevent="submitUser">
        <div class="grid-2">
          <input v-model="firstName" class="input" type="text" :placeholder="t('adminUsers.firstName')" />
          <input v-model="lastName" class="input" type="text" :placeholder="t('adminUsers.lastName')" />
        </div>
        <div class="grid-2">
          <input v-model="email" class="input" type="email" :placeholder="t('adminUsers.email')" />
          <input v-model="phone" class="input" type="tel" :placeholder="t('adminUsers.phone')" />
        </div>
        <div class="grid-2">
          <input v-model="password" class="input" type="password" :placeholder="t('adminUsers.password')" />
          <select v-model="role" class="input">
            <option value="customer">{{ t('adminUsers.roleCustomer') }}</option>
            <option value="technician">{{ t('adminUsers.roleTechnician') }}</option>
            <option value="admin">{{ t('adminUsers.roleAdmin') }}</option>
          </select>
        </div>
        <div class="grid-2">
          <label class="input" style="display:flex; align-items:center; gap:0.5rem;">
            <input v-model="isActive" type="checkbox" />
            {{ t('adminUsers.active') }}
          </label>
        </div>
        <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
          <button class="btn secondary" type="button" @click="goBack">{{ t('adminUsers.back') }}</button>
          <button class="btn" type="submit" :disabled="saving">
            {{ saving ? (editingUserId ? t('adminUsers.updating') : t('adminUsers.creating')) : (editingUserId ? t('adminUsers.updateUser') : t('adminUsers.createUser')) }}
          </button>
          <button v-if="editingUserId" class="btn secondary" type="button" @click="cancelEdit">{{ t('adminUsers.cancelEdit') }}</button>
        </div>
        <p v-if="saveError" class="muted">{{ saveError }}</p>
        <p v-if="saveMessage" class="muted">{{ saveMessage }}</p>
      </form>
      <p v-if="loading" class="muted">{{ t('adminUsers.loading') }}</p>
      <p v-if="error" class="muted">{{ error }}</p>
      <div v-if="users.length" class="table-scroll">
        <table class="table">
          <thead>
            <tr>
              <th>{{ t('adminUsers.headerName') }}</th>
              <th>{{ t('adminUsers.headerEmail') }}</th>
              <th>{{ t('adminUsers.headerRole') }}</th>
              <th>{{ t('adminUsers.headerState') }}</th>
              <th>{{ t('adminUsers.headerActions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.first_name }} {{ u.last_name }}</td>
              <td>{{ u.email }}</td>
              <td><span class="badge">{{ roleLabel(u.role) }}</span></td>
              <td>
                <span class="badge" :class="u.is_active ? '' : 'muted'">
                  {{ u.is_active ? t('adminUsers.activeState') : t('adminUsers.inactiveState') }}
                </span>
              </td>
              <td>
                <button class="btn secondary" type="button" @click="editUser(u)">{{ t('adminUsers.edit') }}</button>
                <button class="btn secondary" style="margin-left: 0.5rem;" type="button" @click="deleteUser(u)">{{ t('adminUsers.delete') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../lib/api'
import Swal from 'sweetalert2'
import { useLanguageStore } from '../stores/language'

const router = useRouter()
const language = useLanguageStore()
const t = language.t
const users = ref([])
const loading = ref(false)
const error = ref('')
const saving = ref(false)
const saveError = ref('')
const saveMessage = ref('')
const editingUserId = ref(null)
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const role = ref('customer')
const isActive = ref(true)

const loadUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/admin/users/')
    users.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || t('adminUsers.errorLoad')
  } finally {
    loading.value = false
  }
}

const fillForm = (u) => {
  firstName.value = u.first_name || ''
  lastName.value = u.last_name || ''
  email.value = u.email || ''
  phone.value = u.phone || ''
  password.value = ''
  role.value = u.role || 'customer'
  isActive.value = u.is_active !== false
}

const editUser = (u) => {
  editingUserId.value = u.id
  saveError.value = ''
  saveMessage.value = ''
  fillForm(u)
}

const roleLabel = (roleValue) => {
  const roleKey = roleValue === 'technician' ? 'roleTechnician' : roleValue === 'admin' ? 'roleAdmin' : 'roleCustomer'
  return t(`adminUsers.${roleKey}`)
}

const deleteUser = async (u) => {
  const result = await Swal.fire({
    title: t('adminUsers.deleteTitle'),
    text: `${t('adminUsers.deletePrompt')} ${u.email}?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: t('adminUsers.deleteConfirm'),
    cancelButtonText: t('adminUsers.deleteCancel'),
    confirmButtonColor: '#d33',
  })

  if (!result.isConfirmed) return

  try {
    await api.delete(`/admin/users/${u.id}`)
    saveMessage.value = t('adminUsers.deleted')
    await Swal.fire({
      title: t('adminUsers.deletedTitle'),
      text: t('adminUsers.deletedText'),
      icon: 'success',
      confirmButtonText: t('adminUsers.deleteOk'),
    })
    if (editingUserId.value === u.id) {
      cancelEdit()
    }
    await loadUsers()
  } catch (err) {
    saveError.value = err.response?.data?.detail || t('adminUsers.deleteError')
    await Swal.fire({
      title: t('adminUsers.deleteErrorTitle'),
      text: saveError.value,
      icon: 'error',
      confirmButtonText: t('adminUsers.deleteOk'),
    })
  }
}

const resetForm = () => {
  editingUserId.value = null
  firstName.value = ''
  lastName.value = ''
  email.value = ''
  phone.value = ''
  password.value = ''
  role.value = 'customer'
  isActive.value = true
}

const cancelEdit = () => {
  resetForm()
  saveError.value = ''
  saveMessage.value = ''
}

const goBack = async () => {
  await router.push('/admin')
}

const submitUser = async () => {
  saving.value = true
  saveError.value = ''
  saveMessage.value = ''
  try {
    const payload = {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      phone: phone.value,
      role: role.value,
      is_active: isActive.value,
    }

    if (editingUserId.value) {
      if (password.value) {
        payload.password = password.value
      }
      await api.patch(`/admin/users/${editingUserId.value}`, payload)
      saveMessage.value = t('adminUsers.updated')
    } else {
      payload.password = password.value
      await api.post('/admin/users/', payload)
      saveMessage.value = t('adminUsers.created')
    }

    cancelEdit()
    await loadUsers()
  } catch (err) {
    saveError.value = err.response?.data?.detail || (editingUserId.value ? t('adminUsers.errorUpdate') : t('adminUsers.errorCreate'))
  } finally {
    saving.value = false
  }
}

onMounted(loadUsers)
</script>
