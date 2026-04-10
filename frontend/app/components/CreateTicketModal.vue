<template>
  <UModal
    :title="$t('tickets.create.modal_title')"
    :close="{ variant: 'outline' }"
    v-model="isOpen"
  >
    <UButton
      icon="i-lucide-plus"
      class="cursor-pointer"
      color="neutral"
      :label="$t('tickets.create.submit')"
      variant="subtle"
    />

    <template #body>
      <div class="modal-content">
        <UForm :state="ticket" @submit="handleSubmit" class="ticket-form">
          <UFormField name="title" :label="$t('tickets.create.title')" required>
            <UInput
              v-model="ticket.title"
              :placeholder="$t('tickets.create.title_placeholder')"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="text" :label="$t('tickets.create.description')">
            <UTextarea
              v-model="ticket.text"
              :placeholder="$t('tickets.create.description_placeholder')"
              :rows="4"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="status" :label="$t('tickets.create.status')">
            <USelect
              v-model="ticket.status"
              :items="statusOptions"
              :placeholder="$t('tickets.create.status_placeholder')"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="project_id" :label="$t('tickets.create.project')">
            <USelectMenu
              v-model="ticket.project_id"
              :items="productionOptions"
              value-key="value"
              :placeholder="$t('tickets.create.project_placeholder')"
              :disabled="isLoading"
              :loading="isLoadingProductions"
            />
          </UFormField>

          <UFormField name="task_id" :label="$t('tickets.create.task_id')">
            <UInput
              v-model="ticket.task_id"
              :placeholder="$t('tickets.create.task_id_placeholder')"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="assignee_id" :label="$t('tickets.create.assignee_id')">
            <UInput
              v-model="ticket.assignee_id"
              :placeholder="$t('tickets.create.assignee_id_placeholder')"
              :disabled="isLoading"
            />
          </UFormField>

          <div class="form-actions">
            <UButton type="submit" color="primary" :loading="isLoading">
              {{ $t('tickets.create.submit') }}
            </UButton>
          </div>
        </UForm>
      </div>
    </template>
  </UModal>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const { getOpenProductions } = useKitsu()

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  productionId: {
    type: String,
    default: null
  },
  episodeId: {
    type: String,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'close'])

const productions = ref([])
const isLoadingProductions = ref(false)

const isOpen = computed({
  get: () => props.modelValue,
  set: (newValue) => {
    emit('update:modelValue', newValue)
    if (!newValue) {
      resetForm()
      emit('close')
    }
  }
})

const ticket = ref({
  title: '',
  text: '',
  status: 'open',
  project_id: null,
  task_id: '',
  assignee_id: ''
})

const statusOptions = computed(() => [
  { label: t('tickets.status.open'), value: 'open' },
  { label: t('tickets.status.on_hold'), value: 'on hold' },
  { label: t('tickets.status.closed'), value: 'closed' }
])

const productionOptions = computed(() =>
  productions.value.map((p) => ({
    label: p.name,
    value: p.id
  }))
)

const fetchProductions = async () => {
  isLoadingProductions.value = true
  try {
    productions.value = await getOpenProductions()
  } catch (error) {
    console.error('Error fetching productions:', error)
    productions.value = []
  } finally {
    isLoadingProductions.value = false
  }
}

const resetForm = () => {
  ticket.value = {
    title: '',
    text: '',
    status: 'open',
    project_id: props.productionId || null,
    task_id: '',
    assignee_id: ''
  }
}

const handleSubmit = () => {
  const emptyToNull = (value) => (value && value.trim() ? value.trim() : null)
  const ticketData = {
    title: ticket.value.title || '',
    text: ticket.value.text || '',
    status: ticket.value.status || 'open',
    task_id: emptyToNull(ticket.value.task_id),
    assignee_id: emptyToNull(ticket.value.assignee_id),
    project_id: ticket.value.project_id || null,
    episode_id: props.episodeId || null
  }
  emit('submit', ticketData)
}

onMounted(() => {
  fetchProductions()
})

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    resetForm()
  }
})

watch(() => props.isLoading, (newValue, oldValue) => {
  if (oldValue === true && newValue === false && props.modelValue) {
    isOpen.value = false
  }
})
</script>

<style scoped>
.ticket-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-primary);
}
</style>
