<template>
  <div class="landing-page">
    <section class="hero container">
      <div class="hero-brand-row">
        <div class="hero-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 96 96" class="hero-brand-logo">
            <circle cx="44" cy="48" r="25" fill="none" stroke="#F56E11" stroke-width="6" />
            <path d="M18 26h52v15H18z" fill="#F56E11" />
            <path d="M31 45l13-13 13 13v22H31z" fill="none" stroke="#082756" stroke-width="6" stroke-linejoin="round" />
            <path d="M37 54h6v8h-6zM49 54h6v8h-6z" fill="#082756" />
          </svg>
        </div>
        <div class="hero-brand-copy">
          <span class="badge">24HR TECH SOLUTIONS</span>
          <p class="muted brand-note">{{ t('landing.heroCopy') }}</p>
        </div>
      </div>

      <div class="hero-inner">
        <div class="card hero-copy landing-copy">
          <h2>
            <span class="title-main">{{ t('landing.heroTitleStart') }}</span>&nbsp;
            <span class="title-accent">{{ t('landing.heroTitleAccent') }}</span>&nbsp;
            <span class="title-main">{{ t('landing.heroTitleEnd') }}</span>
          </h2>
          <p>{{ t('landing.heroCopy') }}</p>
          <div class="review-widget" aria-label="Reseña rápida">
            <div class="review-widget-header">
              <span class="review-label">{{ t('landing.reviewWidget.title') }}</span>
              <span class="review-hint">{{ t('landing.reviewWidget.hint') }}</span>
            </div>

            <div class="star-row" @mouseleave="hoverRating = 0">
              <button
                v-for="star in 5"
                :key="star"
                type="button"
                class="star-button"
                :class="{ active: (hoverRating || selectedRating) >= star }"
                :aria-label="`Valorar con ${star} estrellas`"
                @mouseenter="hoverRating = star"
                @focus="hoverRating = star"
                @click="selectRating(star)"
              >
                ★
              </button>
            </div>

            <transition name="fade-slide">
              <form v-if="selectedRating > 0" class="review-form" @submit.prevent="submitReview">
                <label class="review-form-label" for="review-text">
                  {{ t('landing.reviewWidget.prompt') }}
                </label>
                <input
                  id="review-author"
                  v-model="reviewAuthor"
                  class="input"
                  type="text"
                  :placeholder="t('landing.reviewWidget.namePlaceholder')"
                  maxlength="120"
                />
                <textarea
                  id="review-text"
                  v-model="reviewText"
                  class="input review-textarea"
                  rows="4"
                  :placeholder="t('landing.reviewWidget.textPlaceholder')"
                />
                <button class="btn review-submit" type="submit" :disabled="submittingReview">
                  {{ submittingReview ? t('landing.reviewWidget.sending') : t('landing.reviewWidget.send') }}
                </button>
                <p v-if="reviewMessage" class="review-message" :class="{ error: reviewMessageIsError }">{{ reviewMessage }}</p>
              </form>
            </transition>
          </div>
        </div>

        <aside class="card metrics landing-metrics">
          <div class="metric" v-for="metric in metrics" :key="metric.label">
            <img class="metric-icon" :src="metric.icon" :alt="metric.alt" />
            <div class="metric-copy">
              <strong>{{ metric.value }}</strong>
              <span class="muted">{{ t(metric.label) }}</span>
            </div>
          </div>
        </aside>
      </div>
    </section>

    <section class="section container">
      <div class="grid-2">
        <div class="card content-card">
          <span class="badge">{{ t('common.publicRequest') }}</span>
          <h3>{{ t('landing.requestTitle') }}</h3>
          <p class="muted">{{ t('landing.requestText') }}</p>

          <form class="form-row" @submit.prevent="submitRequest">
            <div class="grid-2">
              <input v-model="customerName" class="input" type="text" :placeholder="t('services.name')" />
              <input v-model="customerPhone" class="input" type="tel" :placeholder="t('services.phone')" />
            </div>
            <div class="grid-2">
              <input v-model="customerEmail" class="input" type="email" :placeholder="t('services.email')" />
              <input v-model="serviceAddress" class="input" type="text" :placeholder="t('services.address')" />
            </div>
            <div class="grid-2">
              <input v-model="postalCode" class="input" type="text" :placeholder="t('services.postalCode')" />
              <input v-model="title" class="input" type="text" :placeholder="t('services.type')" />
            </div>
            <input v-model="scheduledDate" class="input" type="datetime-local" :aria-label="t('services.date')" />
            <textarea v-model="description" class="input" rows="4" :placeholder="t('services.description')"></textarea>
            <button class="btn" type="submit" :disabled="saving">{{ saving ? t('services.submitting') : t('landing.requestButton') }}</button>
            <p v-if="saveMessage" class="muted">{{ saveMessage }}</p>
            <p v-if="saveError" class="muted">{{ saveError }}</p>
          </form>
        </div>

        <div class="card content-card">
          <span class="badge">{{ t('landing.nextTitle') }}</span>
          <h3>{{ t('landing.nextTitle') }}</h3>
          <p class="muted">{{ t('landing.nextText') }}</p>
          <div class="metric flow-step">
            <strong>1</strong>
            <span class="muted">{{ t('landing.steps.0') }}</span>
          </div>
          <div class="metric flow-step">
            <strong>2</strong>
            <span class="muted">{{ t('landing.steps.1') }}</span>
          </div>
          <div class="metric flow-step">
            <strong>3</strong>
            <span class="muted">{{ t('landing.steps.2') }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section container services-showcase-wrap">
      <div class="card services-showcase" :aria-label="t('landing.servicesSection.badge')">
        <div class="services-showcase-header">
          <span class="badge">{{ t('landing.servicesSection.badge') }}</span>
          <h3>{{ t('landing.servicesSection.title') }}</h3>
        </div>

        <div class="services-showcase-grid">
          <article class="showcase-item" v-for="item in serviceItems" :key="item.key">
            <div class="showcase-icon" :style="{ color: item.color }" v-html="item.icon" />
            <div class="showcase-copy">
              <h4>{{ t(`landing.servicesSection.items.${item.key}.title`) }}</h4>
              <p>{{ t(`landing.servicesSection.items.${item.key}.description`) }}</p>
            </div>
          </article>
        </div>

        <div class="services-benefits" role="list" :aria-label="t('landing.servicesSection.benefitsLabel')">
          <div class="benefit-pill" role="listitem" v-for="benefit in benefits" :key="benefit">
            {{ t(`landing.servicesSection.benefits.${benefit}`) }}
          </div>
        </div>
      </div>
    </section>

    <section class="section container reviews-section-wrap">
      <div class="card reviews-section">
        <div class="reviews-section-header">
          <span class="badge">{{ t('landing.reviewsSection.badge') }}</span>
          <h3>{{ t('landing.reviewsSection.title') }}</h3>
          <p class="muted">{{ t('landing.reviewsSection.subtitle') }}</p>
        </div>

        <p v-if="reviewsLoading && !publicReviews.length" class="muted reviews-status">{{ t('landing.reviewsSection.loading') }}</p>
        <p v-else-if="reviewsError" class="muted reviews-status error">{{ reviewsError }}</p>
        <p v-else-if="!publicReviews.length" class="muted reviews-status">{{ t('landing.reviewsSection.empty') }}</p>

        <div v-else class="reviews-grid">
          <article class="review-card" v-for="review in publicReviews" :key="review.id">
            <header class="review-card-head">
              <div class="review-stars" :aria-label="`${review.rating} de 5`">
                <span v-for="star in 5" :key="`${review.id}-${star}`" :class="{ active: star <= Number(review.rating) }">★</span>
              </div>
              <strong>{{ review.rating }}/5</strong>
            </header>
            <p class="review-comment">{{ review.comment }}</p>
            <footer class="review-meta">
              <span>{{ review.author_name || t('landing.reviewsSection.anonymous') }}</span>
              <span>{{ formatReviewDate(review.created_at) }}</span>
            </footer>
          </article>
        </div>

        <div v-if="reviewsTotalPages > 1" class="reviews-pagination" aria-label="Paginación de reseñas">
          <button
            class="btn secondary"
            type="button"
            :disabled="reviewsLoading || reviewsPage <= 1"
            @click="changeReviewPage(reviewsPage - 1)"
          >
            {{ t('landing.reviewsSection.prev') }}
          </button>
          <span class="muted">{{ t('landing.reviewsSection.page') }} {{ reviewsPage }} / {{ reviewsTotalPages }}</span>
          <button
            class="btn secondary"
            type="button"
            :disabled="reviewsLoading || reviewsPage >= reviewsTotalPages"
            @click="changeReviewPage(reviewsPage + 1)"
          >
            {{ t('landing.reviewsSection.next') }}
          </button>
        </div>
      </div>
    </section>

    <footer class="landing-footer">
      <div class="container footer-grid">
        <div class="footer-brand-block">
          <img class="footer-logo" :src="techSolutionsLogo" alt="TECH SOLUTIONS" />
          <p>{{ t('landing.footerText') }}</p>
        </div>

        <div>
          <h4>{{ t('landing.quickLinks') }}</h4>
          <ul>
            <li><a href="#">{{ t('nav.home') }}</a></li>
            <li><a href="#">{{ t('nav.service') }}</a></li>
            <li><a href="#">{{ t('landing.aboutUs') }}</a></li>
            <li><a href="#">{{ t('landing.howItWorks') }}</a></li>
            <li><a href="#">{{ t('landing.contactLink') }}</a></li>
          </ul>
        </div>

        <div>
          <h4>{{ t('landing.servicesListTitle') }}</h4>
          <ul>
            <li>{{ t('landing.serviceItems.hvac') }}</li>
            <li>{{ t('landing.serviceItems.electricity') }}</li>
            <li>{{ t('landing.serviceItems.plumbing') }}</li>
            <li>{{ t('landing.serviceItems.security') }}</li>
            <li>{{ t('landing.serviceItems.automation') }}</li>
            <li>{{ t('landing.serviceItems.maintenance') }}</li>
          </ul>
        </div>

        <div>
          <h4>{{ t('landing.contactTitle') }}</h4>
          <ul>
            <li>407-955-3435</li>
            <li>Techsolutionsnow@gmail.com</li>
            <li>Florida, USA</li>
            <li>{{ t('landing.serviceItems.support') }}</li>
          </ul>
        </div>
      </div>

      <div class="container footer-copy">{{ t('landing.copyright') }}</div>
    </footer>

    <a
      class="whatsapp-float"
      href="https://wa.me/14079553435"
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Abrir chat de WhatsApp"
      title="WhatsApp"
    >
      <img :src="whatsAppLogo" alt="WhatsApp" />
    </a>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../lib/api'
import clockIcon from '../assets/clock.png'
import peopleIcon from '../assets/people.png'
import chronometerIcon from '../assets/chronometer.png'
import techSolutionsLogo from '../assets/Logo TECH SOLUTIONS 1.png'
import whatsAppLogo from '../assets/whatsapp.png'
import { useLanguageStore } from '../stores/language'

const language = useLanguageStore()
const t = language.t
const customerName = ref('')
const customerPhone = ref('')
const customerEmail = ref('')
const serviceAddress = ref('')
const postalCode = ref('')
const title = ref('')
const description = ref('')
const scheduledDate = ref('')
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref('')
const selectedRating = ref(0)
const hoverRating = ref(0)
const reviewAuthor = ref('')
const reviewText = ref('')
const reviewMessage = ref('')
const reviewMessageIsError = ref(false)
const submittingReview = ref(false)
const publicReviews = ref([])
const reviewsPage = ref(1)
const reviewsTotalPages = ref(0)
const reviewsLoading = ref(false)
const reviewsError = ref('')

const metrics = [
  {
    value: '24/7',
    label: 'landing.metrics.support',
    icon: clockIcon,
    alt: 'Icono de atención de emergencias',
  },
  {
    value: '500+',
    label: 'landing.metrics.completed',
    icon: peopleIcon,
    alt: 'Icono de servicios completados',
  },
  {
    value: '60 min',
    label: 'landing.metrics.response',
    icon: chronometerIcon,
    alt: 'Icono de tiempo promedio de respuesta',
  },
]

const selectRating = (rating) => {
  selectedRating.value = rating
  reviewMessage.value = ''
  reviewMessageIsError.value = false
}

const formatReviewDate = (value) => {
  if (!value) {
    return ''
  }

  try {
    return new Intl.DateTimeFormat(language.locale === 'en' ? 'en-US' : 'es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(new Date(value))
  } catch {
    return ''
  }
}

const loadPublicReviews = async (page = 1) => {
  reviewsLoading.value = true
  reviewsError.value = ''

  try {
    const { data } = await api.get('/reviews/public', {
      params: { page },
    })
    publicReviews.value = data.items || []
    reviewsPage.value = data.page || 1
    reviewsTotalPages.value = data.total_pages || 0
  } catch (err) {
    reviewsError.value = err.response?.data?.detail || t('landing.reviewsSection.loadError')
  } finally {
    reviewsLoading.value = false
  }
}

const changeReviewPage = async (nextPage) => {
  if (nextPage < 1 || (reviewsTotalPages.value > 0 && nextPage > reviewsTotalPages.value)) {
    return
  }
  await loadPublicReviews(nextPage)
}

const submitReview = async () => {
  if (!reviewText.value.trim()) {
    reviewMessage.value = t('landing.reviewWidget.empty')
    reviewMessageIsError.value = true
    return
  }

  if (selectedRating.value < 1) {
    reviewMessage.value = t('landing.reviewWidget.ratingRequired')
    reviewMessageIsError.value = true
    return
  }

  submittingReview.value = true
  reviewMessage.value = ''

  try {
    await api.post('/reviews/public', {
      author_name: reviewAuthor.value,
      rating: selectedRating.value,
      comment: reviewText.value,
    })
    reviewMessage.value = t('landing.reviewWidget.success')
    reviewMessageIsError.value = false
    reviewAuthor.value = ''
    reviewText.value = ''
    selectedRating.value = 0
    hoverRating.value = 0
    await loadPublicReviews(1)
  } catch (err) {
    reviewMessage.value = err.response?.data?.detail || t('landing.reviewWidget.error')
    reviewMessageIsError.value = true
  } finally {
    submittingReview.value = false
  }
}

const serviceItems = [
  {
    key: 'hvac',
    color: '#1f7ecf',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2V22M4.9 6L19.1 18M4.9 18L19.1 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
  },
  {
    key: 'electrical',
    color: '#f56e11',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M13.2 2L6 13H11L10.8 22L18 11H13L13.2 2Z" fill="currentColor"/></svg>`,
  },
  {
    key: 'plumbing',
    color: '#2c86d8',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 4V9H10.5V6H13.5V9H17V14.4C17 17.5 14.5 20 11.4 20H10.6C7.5 20 5 17.5 5 14.4V12H9V10H5V4H7Z" fill="currentColor"/></svg>`,
  },
  {
    key: 'security',
    color: '#082756',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 12L21 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M6 12L10 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M11 13L15 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M16 17L20 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
  },
  {
    key: 'smartHome',
    color: '#f56e11',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 11.5L12 4L20 11.5V19.5H14.8V14.5H9.2V19.5H4V11.5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`,
  },
  {
    key: 'handyman',
    color: '#082756',
    icon: `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 6L9 10M15 14L19 18M7 17L17 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M16.5 4.5L19.5 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
  },
]

const benefits = ['certified', 'attention24h', 'transparentQuotes', 'serviceWarranty', 'bilingualSupport']

const submitRequest = async () => {
  saving.value = true
  saveMessage.value = ''
  saveError.value = ''

  try {
    const payload = {
      customer_name: customerName.value,
      customer_phone: customerPhone.value,
      customer_email: customerEmail.value,
      service_address: serviceAddress.value,
      postal_code: postalCode.value,
      title: title.value,
      description: description.value,
      scheduled_date: scheduledDate.value ? new Date(scheduledDate.value).toISOString() : null,
    }
    const { data } = await api.post('/services/public', payload)
    saveMessage.value = `${t('landing.requestSuccess')} ${data.tracking_code}.`
    customerName.value = ''
    customerPhone.value = ''
    customerEmail.value = ''
    serviceAddress.value = ''
    postalCode.value = ''
    title.value = ''
    description.value = ''
    scheduledDate.value = ''
  } catch (err) {
    saveError.value = err.response?.data?.detail || t('landing.requestError')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await loadPublicReviews(1)
})
</script>

<style scoped>
.review-widget {
  margin-top: 1.5rem;
  padding: 1.1rem 1.1rem 1rem;
  border-radius: 24px;
  border: 1px solid rgba(8, 39, 86, 0.12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  box-shadow: 0 14px 30px rgba(8, 39, 86, 0.06);
}

.review-widget-header {
  display: grid;
  gap: 0.2rem;
  margin-bottom: 0.8rem;
}

.review-label {
  color: #082756;
  font-size: 1.02rem;
  font-weight: 800;
}

.review-hint {
  color: #5d6676;
  font-size: 0.95rem;
}

.star-row {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.star-button {
  appearance: none;
  border: 0;
  background: transparent;
  padding: 0;
  font-size: 2rem;
  line-height: 1;
  color: rgba(8, 39, 86, 0.22);
  cursor: pointer;
  transition: transform 160ms ease, color 160ms ease, filter 160ms ease;
}

.star-button:hover,
.star-button:focus-visible,
.star-button.active {
  color: #f5b301;
  filter: drop-shadow(0 8px 12px rgba(245, 179, 1, 0.2));
}

.star-button:hover,
.star-button:focus-visible {
  transform: translateY(-1px) scale(1.08);
}

.review-form {
  display: grid;
  gap: 0.8rem;
  margin-top: 0.9rem;
}

.review-form-label {
  color: #082756;
  font-weight: 700;
}

.review-textarea {
  resize: vertical;
  min-height: 7rem;
}

.review-submit {
  width: fit-content;
}

.review-message {
  margin: 0;
  color: #138a36;
  font-weight: 600;
}

.review-message.error {
  color: #b42318;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.services-showcase-wrap {
  padding-top: 0;
}

.reviews-section-wrap {
  padding-top: 0;
}

.reviews-section {
  padding: 1.2rem;
  border-radius: 26px;
  background: #ffffff;
}

.reviews-section-header {
  display: grid;
  gap: 0.35rem;
  margin-bottom: 1rem;
}

.reviews-section-header h3 {
  margin: 0;
  color: #082756;
  font-size: clamp(1.2rem, 2.2vw, 2rem);
}

.reviews-status {
  margin: 0;
}

.reviews-status.error {
  color: #b42318;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.8rem;
}

.review-card {
  border: 1px solid rgba(8, 39, 86, 0.11);
  border-radius: 18px;
  padding: 0.95rem;
  background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
  box-shadow: 0 10px 24px rgba(8, 39, 86, 0.05);
}

.review-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.7rem;
  margin-bottom: 0.55rem;
}

.review-card-head strong {
  color: #082756;
}

.review-stars {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  color: rgba(8, 39, 86, 0.2);
}

.review-stars .active {
  color: #f5b301;
}

.review-comment {
  margin: 0;
  color: #4f596a;
  line-height: 1.45;
}

.review-meta {
  margin-top: 0.7rem;
  padding-top: 0.65rem;
  border-top: 1px solid rgba(8, 39, 86, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  color: #667085;
  font-size: 0.9rem;
}

.reviews-pagination {
  margin-top: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.reviews-pagination .btn.secondary {
  min-width: 8rem;
  border-radius: 999px;
}

.services-showcase {
  padding: 1.2rem;
  border-radius: 26px;
  background: #ffffff;
}

.services-showcase-header {
  display: grid;
  justify-items: center;
  gap: 0.35rem;
  margin-bottom: 0.95rem;
  text-align: center;
}

.services-showcase-header .badge {
  background: rgba(245, 110, 17, 0.12);
  color: #f56e11;
}

.services-showcase-header h3 {
  margin: 0;
  color: #082756;
  font-size: clamp(1.2rem, 2.2vw, 2rem);
}

.services-showcase-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
}

.showcase-item {
  border: 1px solid rgba(8, 39, 86, 0.1);
  border-radius: 18px;
  padding: 0.95rem;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
}

.showcase-icon {
  width: 2.05rem;
  height: 2.05rem;
}

.showcase-icon :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

.showcase-copy h4 {
  margin: 0;
  color: #082756;
  font-size: 1.05rem;
}

.showcase-copy p {
  margin: 0.25rem 0 0;
  color: #5d6676;
  line-height: 1.45;
}

.services-benefits {
  margin-top: 0.85rem;
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.55rem;
}

.benefit-pill {
  min-height: 3.25rem;
  border-radius: 14px;
  border: 1px solid rgba(8, 39, 86, 0.12);
  background: #f8fafe;
  display: grid;
  place-items: center;
  text-align: center;
  color: #082756;
  font-weight: 700;
  line-height: 1.3;
  padding: 0.5rem 0.55rem;
}

.whatsapp-float {
  position: fixed;
  right: 1.1rem;
  bottom: 1.1rem;
  z-index: 40;
  width: 3.6rem;
  height: 3.6rem;
  display: grid;
  place-items: center;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  overflow: visible;
  padding: 0;
  transition: transform 160ms ease;
}

.whatsapp-float img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
}

.whatsapp-float:hover {
  transform: translateY(-2px) scale(1.03);
}

@media (max-width: 640px) {
  .services-showcase {
    padding: 0.9rem;
    border-radius: 20px;
  }

  .services-showcase-grid {
    grid-template-columns: 1fr;
  }

  .reviews-section {
    padding: 0.9rem;
    border-radius: 20px;
  }

  .reviews-grid {
    grid-template-columns: 1fr;
  }

  .review-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .services-benefits {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .whatsapp-float {
    right: 0.85rem;
    bottom: 0.85rem;
    width: 3.2rem;
    height: 3.2rem;
  }
}

@media (min-width: 641px) and (max-width: 960px) {
  .services-showcase-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .reviews-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .services-benefits {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>
