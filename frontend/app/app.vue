<script setup>
const route = useRoute()

const applyTheme = (dark) => {
  document.documentElement.classList.toggle('dark', dark)
}

// Apply theme from query param
watch(() => route.query.dark_theme, (value) => {
  applyTheme(value === 'true')
}, { immediate: true })

// Listen for theme changes from parent Kitsu window
onMounted(() => {
  window.addEventListener('message', (event) => {
    if (event.data && 'dark_theme' in event.data) {
      applyTheme(!!event.data.dark_theme)
    }
  })
})

useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

const title = 'Ticket plugin'
const description = 'Ticket system to add issue tracking to Kitsu tasks.'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description,
  twitterCard: 'summary_large_image'
})
</script>

<template>
  <UApp>
    <UMain>
      <NuxtPage />
    </UMain>
  </UApp>
</template>
