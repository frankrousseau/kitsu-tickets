import { createI18n } from 'vue-i18n'
import en from '~/locales/en.js'
import fr from '~/locales/fr.js'

export default defineNuxtPlugin((nuxtApp) => {
  const locale =
    new URLSearchParams(window.location.search).get('locale') || 'en'

  const i18n = createI18n({
    legacy: false,
    locale,
    fallbackLocale: 'en',
    messages: { en, fr }
  })

  nuxtApp.vueApp.use(i18n)
})
