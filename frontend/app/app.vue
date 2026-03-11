<script setup>
const route = useRoute()
const colorMode = useColorMode()

const isDarkTheme = computed(() => route.query.dark_theme === 'true')

watch(isDarkTheme, (dark) => {
  colorMode.preference = dark ? 'dark' : 'light'
}, { immediate: true })

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
const description = 'Ticket systems to add issue tracking to Kitsu tasks.'

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
