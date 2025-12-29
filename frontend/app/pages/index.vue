<template>
  <div class="tickets-container">
    <div class="tickets-header">
      <div class="header-content">
        <p v-if="tickets.length > 0" class="tickets-count">
          {{ tickets.length }} ticket{{ tickets.length !== 1 ? 's' : '' }} found
        </p>
        <button
          class="button is-primary"
          @click="isCreateModalOpen = true"
        >
          <span class="icon">
            <Icon icon="lucide:plus" />
          </span>
          <span>Create Ticket</span>
        </button>
      </div>
    </div>

    <div v-if="tickets.length === 0 && !isLoading" class="empty-state">
      <span class="icon empty-icon">
        <Icon icon="lucide:ticket" width="64" height="64" />
      </span>
      <p class="empty-text">No tickets found</p>
    </div>

    <div v-else class="tickets-list">
      <div
        v-for="ticket in tickets"
        :key="ticket.id || Math.random()"
        class="card ticket-card"
      >
        <div class="card-content ticket-content">
          <div class="ticket-header">
            <h3 class="title is-5 ticket-title">{{ ticket.title || 'Untitled Ticket' }}</h3>
            <span
              :class="['tag', 'status-badge', `is-${getStatusColor(ticket.status)}`]"
            >
              {{ formatStatus(ticket.status) }}
            </span>
          </div>

          <p v-if="ticket.text" class="ticket-text">
            {{ ticket.text }}
          </p>

          <div class="ticket-footer">
            <div class="ticket-meta">
              <span v-if="ticket.task_id" class="meta-item">
                <span class="icon is-small">
                  <Icon icon="lucide:clipboard-list" />
                </span>
                <span class="meta-label">Task:</span>
                <span class="meta-value">{{ formatId(ticket.task_id) }}</span>
              </span>
              <span v-if="ticket.person_id" class="meta-item">
                <span class="icon is-small">
                  <Icon icon="lucide:user-plus" />
                </span>
                <span class="meta-label">Created by:</span>
                <span class="meta-value">{{ formatId(ticket.person_id) }}</span>
              </span>
              <span v-if="ticket.assignee_id" class="meta-item">
                <span class="icon is-small">
                  <Icon icon="lucide:user-check" />
                </span>
                <span class="meta-label">Assigned to:</span>
                <span class="meta-value">{{ formatId(ticket.assignee_id) }}</span>
              </span>
            </div>
            <div class="ticket-dates">
              <div v-if="ticket.created_at" class="ticket-date">
                <span class="icon is-small">
                  <Icon icon="lucide:calendar-plus" />
                </span>
                <span class="meta-label">Created:</span>
                <span>{{ formatDate(ticket.created_at) }}</span>
              </div>
              <div v-if="ticket.updated_at && ticket.updated_at !== ticket.created_at" class="ticket-date">
                <span class="icon is-small">
                  <Icon icon="lucide:calendar-clock" />
                </span>
                <span class="meta-label">Updated:</span>
                <span>{{ formatDate(ticket.updated_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Ticket Modal -->
  <div
    :class="['modal', { 'is-active': isCreateModalOpen }]"
    @click.self="isCreateModalOpen = false"
  >
    <div class="modal-background" @click="isCreateModalOpen = false"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create New Ticket</p>
        <button
          class="delete"
          aria-label="close"
          @click="isCreateModalOpen = false"
        ></button>
      </header>

      <section class="modal-card-body">
        <form @submit.prevent="handleCreateTicket" class="ticket-form">
          <div class="field">
            <label class="label">Title <span class="has-text-danger">*</span></label>
            <div class="control">
              <input
                v-model="newTicket.title"
                class="input"
                type="text"
                placeholder="Enter ticket title"
                :disabled="isCreating"
                required
              />
            </div>
          </div>

          <div class="field">
            <label class="label">Description</label>
            <div class="control">
              <textarea
                v-model="newTicket.text"
                class="textarea"
                placeholder="Enter ticket description"
                rows="4"
                :disabled="isCreating"
              ></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="newTicket.status" :disabled="isCreating">
                  <option
                    v-for="option in statusOptions"
                    :key="option.value"
                    :value="option.value"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Task ID</label>
            <div class="control">
              <input
                v-model="newTicket.task_id"
                class="input"
                type="text"
                placeholder="Enter task ID (optional)"
                :disabled="isCreating"
              />
            </div>
          </div>

          <div class="field">
            <label class="label">Assignee ID</label>
            <div class="control">
              <input
                v-model="newTicket.assignee_id"
                class="input"
                type="text"
                placeholder="Enter assignee ID (optional)"
                :disabled="isCreating"
              />
            </div>
          </div>

          <div class="field is-grouped form-actions">
            <div class="control">
              <button
                type="button"
                class="button"
                @click="isCreateModalOpen = false"
                :disabled="isCreating"
              >
                Cancel
              </button>
            </div>
            <div class="control">
              <button
                type="submit"
                class="button is-primary"
                :class="{ 'is-loading': isCreating }"
                :disabled="isCreating"
              >
                Create Ticket
              </button>
            </div>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'

/**
 * Ticket data structure based on the Ticket model from models.py
 *
 * Fields from Ticket model:
 * - title: Text (optional)
 * - text: Text (optional)
 * - status: Enum (TicketStatus: OPEN="open", ON_HOLD="on hold", CLOSED="closed")
 * - task_id: UUID, ForeignKey to task.id (optional)
 * - person_id: UUID, ForeignKey to person.id (required - creator/author)
 * - assignee_id: UUID, ForeignKey to person.id (optional)
 *
 * Fields from BaseMixin:
 * - id: UUID
 * - created_at: DateTime
 * - updated_at: DateTime
 */

const route = useRoute()

const { client, fetchTickets, createTicket } = useKitsu()

const isLoggedIn = ref(null)
const openProductions = ref([])
const tickets = ref([])
const isLoading = ref(true)
const isCreateModalOpen = ref(false)
const isCreating = ref(false)

const newTicket = ref({
  title: '',
  text: '',
  status: 'open',
  task_id: '',
  assignee_id: ''
})

const statusOptions = [
  { label: 'Open', value: 'open' },
  { label: 'On Hold', value: 'on hold' },
  { label: 'Closed', value: 'closed' }
]

const productionId = computed(() => route.query.production_id)
const episodeId = computed(() => route.query.episode_id)
const isDarkTheme = computed(() => route.query.dark_theme === 'true')
const isStudioPage = computed(() => !productionId.value && !episodeId.value)

onMounted(() => {
  console.log(productionId.value)
  fetchData()
})

const fetchData = async () => {
  try {
    isLoading.value = true
    console.log('fetching data')
    const isLoggedInResponse = await client.isLoggedIn()
    isLoggedIn.value = isLoggedInResponse.isLoggedIn
    console.log(isLoggedInResponse)

    const openProductionsResponse = await client.getOpenProductions()
    console.log(openProductionsResponse)
    openProductions.value = openProductionsResponse
    console.log(openProductionsResponse)

    const ticketsResponse = await fetchTickets(productionId.value, episodeId.value)
    console.log(ticketsResponse)
    tickets.value = ticketsResponse || []
    console.log(ticketsResponse)
  } catch (error) {
    console.error('Error fetching data:', error)
    tickets.value = []
  } finally {
    isLoading.value = false
  }
}

/**
 * Get status color based on TicketStatus enum values:
 * - OPEN = "open" -> success (green)
 * - ON_HOLD = "on hold" -> warning (yellow)
 * - CLOSED = "closed" -> neutral (gray)
 */
const getStatusColor = (status) => {
  if (!status) return 'info'
  const statusLower = status.toLowerCase()
  if (statusLower === 'open') return 'success'
  if (statusLower === 'on hold') return 'warning'
  if (statusLower === 'closed') return 'dark'
  return 'info'
}

/**
 * Format date string to readable format
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

/**
 * Format UUID to shorter display format (first 8 characters)
 */
const formatId = (id) => {
  if (!id) return ''
  // Show first 8 characters of UUID for readability
  return id.substring(0, 8) + '...'
}

/**
 * Format status for display (capitalize first letter)
 */
const formatStatus = (status) => {
  if (!status) return 'Unknown'
  // Capitalize first letter of each word
  return status.split(' ').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ')
}

/**
 * Handle creating a new ticket
 */
const handleCreateTicket = async () => {
  try {
    isCreating.value = true

    // Prepare ticket data
    // Note: person_id is required but may be set automatically by the backend from JWT token
    const ticketData = {
      title: newTicket.value.title || null,
      text: newTicket.value.text || null,
      status: newTicket.value.status || 'open',
      task_id: newTicket.value.task_id || null,
      assignee_id: newTicket.value.assignee_id || null
    }

    // Remove empty strings and convert to null
    Object.keys(ticketData).forEach(key => {
      if (ticketData[key] === '') {
        ticketData[key] = null
      }
    })

    // Create the ticket
    const createdTicket = await createTicket(ticketData)
    console.log('Ticket created:', createdTicket)

    // Reset form
    newTicket.value = {
      title: '',
      text: '',
      status: 'open',
      task_id: '',
      assignee_id: ''
    }

    // Close modal
    isCreateModalOpen.value = false

    // Refresh tickets list
    await fetchData()
  } catch (error) {
    console.error('Error creating ticket:', error)
    // You might want to show an error notification here
    alert('Failed to create ticket: ' + (error.message || 'Unknown error'))
  } finally {
    isCreating.value = false
  }
}
</script>
