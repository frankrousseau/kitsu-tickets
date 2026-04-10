<template>
  <div v-if="isLoading" class="loading-state">
    <UIcon name="i-lucide-loader-circle" class="animate-spin" size="24" />
    <span>{{ $t('tickets.loading') }}</span>
  </div>

  <div v-else-if="!isLoggedIn" class="empty-state">
    <UIcon name="i-lucide-log-in" size="48" />
    <p class="empty-text">{{ $t('tickets.not_logged_in') }}</p>
  </div>

  <div v-else class="tickets-container">
    <div class="tickets-header">
      <div class="header-content">
        <div>
          <h1 class="tickets-title">{{ $t('tickets.title') }}</h1>
          <p class="tickets-count">
            {{ $t('tickets.count', filteredTickets.length) }}
            <span v-if="isStudioPage"> {{ $t('tickets.all_productions') }}</span>
          </p>
        </div>
        <CreateTicketModal
          :is-loading="isCreating"
          :production-id="productionId"
          :episode-id="episodeId"
          v-model="isCreateModalOpen"
          @submit="handleCreateTicket"
          @close="closeModal"
        />
      </div>
    </div>

    <TicketList
      :tickets="filteredTickets"
      :productions="productions"
      :deleting-ticket-id="deletingTicketId"
      @delete="handleDeleteTicket"
    />
  </div>
</template>

<script setup>
const route = useRoute()

const { client, getOpenProductions, fetchTickets, createTicket, deleteTicket } = useKitsu()

const isLoggedIn = ref(null)
const tickets = ref([])
const productions = ref([])
const isLoading = ref(true)
const isCreateModalOpen = ref(false)
const isCreating = ref(false)
const deletingTicketId = ref(null)

const productionId = computed(() => route.query.production_id)
const episodeId = computed(() => route.query.episode_id)
const isStudioPage = computed(() => !productionId.value && !episodeId.value)

onMounted(() => {
  fetchData()
})

const filteredTickets = computed(() => {
  return tickets.value.filter((ticket) => {
    if (isStudioPage.value) {
      return true
    } else if (episodeId.value) {
      return (
        ticket.project_id === productionId.value
        && ticket.episode_id === episodeId.value
      )
    } else if (productionId.value) {
      return ticket.project_id === productionId.value
    }
    return true
  })
})

const fetchData = async () => {
  try {
    isLoading.value = true
    const isLoggedInResponse = await client.isLoggedIn()
    isLoggedIn.value = isLoggedInResponse.isLoggedIn
    const [ticketsData, productionsData] = await Promise.all([
      fetchTickets(productionId.value, episodeId.value),
      getOpenProductions()
    ])
    tickets.value = ticketsData
    productions.value = productionsData
  } catch (error) {
    console.error('Error fetching data:', error)
    tickets.value = []
  } finally {
    isLoading.value = false
  }
}

const handleCreateTicket = async (ticketData) => {
  try {
    isCreating.value = true
    const createdTicket = await createTicket(ticketData)
    tickets.value.unshift(createdTicket)
  } catch (error) {
    console.error('Error creating ticket:', error)
  } finally {
    isCreating.value = false
  }
}

const closeModal = () => {
  isCreateModalOpen.value = false
}

const handleDeleteTicket = async (ticket) => {
  deletingTicketId.value = ticket.id
  try {
    await deleteTicket(ticket.id)
    tickets.value = tickets.value.filter((t) => t.id !== ticket.id)
  } catch (error) {
    console.error('Error deleting ticket:', error)
  } finally {
    deletingTicketId.value = null
  }
}
</script>
