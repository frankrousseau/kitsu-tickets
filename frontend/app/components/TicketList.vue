<template>
  <div v-if="tickets.length === 0" class="empty-state">
    <UIcon name="i-lucide-ticket" class="empty-icon" />
    <p class="empty-text">{{ $t('tickets.no_tickets') }}</p>
  </div>

  <div v-else class="tickets-list">
    <UCard
      v-for="ticket in tickets"
      :key="ticket.id"
      class="ticket-card"
    >
      <div class="ticket-content">
        <div class="ticket-header">
          <h3 class="ticket-title">
            {{ ticket.title || $t('tickets.untitled') }}
          </h3>
          <div class="flex items-center gap-2">
            <UBadge
              :color="getStatusColor(ticket.status)"
              variant="subtle"
              class="status-badge"
            >
              {{ formatStatus(ticket.status) }}
            </UBadge>
            <UButton
              class="cursor-pointer"
              icon="i-lucide-trash-2"
              color="red"
              variant="ghost"
              size="xs"
              :loading="props.deletingTicketId === ticket.id"
              @click="handleDelete(ticket)"
            />
          </div>
        </div>

        <p v-if="ticket.text" class="ticket-text">
          {{ ticket.text }}
        </p>

        <div class="ticket-footer">
          <div class="ticket-meta">
            <span v-if="ticket.task_id" class="meta-item">
              <UIcon name="i-lucide-clipboard-list" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.task') }}</span>
              <span class="meta-value">
                {{ formatId(ticket.task_id) }}
              </span>
            </span>
            <span v-if="ticket.person_id" class="meta-item">
              <UIcon name="i-lucide-user-plus" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.created_by') }}</span>
              <span class="meta-value">
                {{ formatId(ticket.person_id) }}
              </span>
            </span>
            <span v-if="ticket.assignee_id" class="meta-item">
              <UIcon name="i-lucide-user-check" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.assigned_to') }}</span>
              <span class="meta-value">
                {{ formatId(ticket.assignee_id) }}
              </span>
            </span>
            <span v-if="ticket.project_id" class="meta-item">
              <UIcon name="i-lucide-factory" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.production') }}</span>
              <span class="meta-value">
                {{ productionName(ticket.project_id) }}
              </span>
            </span>
            <span v-if="ticket.episode_id" class="meta-item">
              <UIcon name="i-lucide-tv" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.episode') }}</span>
              <span class="meta-value">
                {{ formatId(ticket.episode_id) }}
              </span>
            </span>
          </div>
          <div class="ticket-dates">
            <div v-if="ticket.created_at" class="ticket-date">
              <UIcon name="i-lucide-calendar-plus" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.created') }}</span>
              <span>{{ formatDate(ticket.created_at) }}</span>
            </div>
            <div
              v-if="
                ticket.updated_at && ticket.updated_at !== ticket.created_at
              "
              class="ticket-date"
            >
              <UIcon name="i-lucide-calendar-clock" class="meta-icon" />
              <span class="meta-label">{{ $t('tickets.fields.updated') }}</span>
              <span>{{ formatDate(ticket.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </UCard>
    <div class="footer flex items-center">
      <p class="tickets-count text-center">{{ $t('tickets.count', tickets.length) }}</p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  tickets: {
    type: Array,
    required: true,
    default: () => []
  },
  productions: {
    type: Array,
    default: () => []
  },
  deletingTicketId: {
    type: String,
    default: null
  }
})

const productionMap = computed(() => {
  const map = {}
  for (const p of props.productions) {
    map[p.id] = p.name
  }
  return map
})

const productionName = (id) => {
  return productionMap.value[id] || formatId(id)
}

const emit = defineEmits(['delete'])

const handleDelete = (ticket) => {
  if (!ticket.id) return
  emit('delete', ticket)
}

const statusMap = {
  open: 'tickets.status.open',
  'on hold': 'tickets.status.on_hold',
  closed: 'tickets.status.closed'
}

const getStatusColor = (status) => {
  if (!status) return 'info'
  const s = status.toLowerCase()
  if (s === 'open') return 'success'
  if (s === 'on hold') return 'warning'
  if (s === 'closed') return 'neutral'
  return 'info'
}

const formatStatus = (status) => {
  if (!status) return status
  const key = statusMap[status.toLowerCase()]
  return key ? t(key) : status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString(undefined, {
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

const formatId = (id) => {
  if (!id) return ''
  return id.substring(0, 8) + '...'
}
</script>
