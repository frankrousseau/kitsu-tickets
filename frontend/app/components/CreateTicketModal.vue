<template>
  <UModal
    title="Create New Ticket"
    :close="{ variant: 'outline' }"
    v-model="isOpen"
  >
    <UButton
      icon="i-lucide-plus"
      class="cursor-pointer"
      color="neutral"
      label="Create Ticket"
      variant="subtle"
    />

    <template #body>
      <div class="modal-content">
        <UForm :state="ticket" @submit="handleSubmit" class="ticket-form">
          <UFormField name="title" label="Title" required>
            <UInput
              v-model="ticket.title"
              placeholder="Enter ticket title"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="text" label="Description">
            <UTextarea
              v-model="ticket.text"
              placeholder="Enter ticket description"
              :rows="4"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="status" label="Status">
            <USelect
              v-model="ticket.status"
              :options="statusOptions"
              placeholder="Select status"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="task_id" label="Task ID">
            <UInput
              v-model="ticket.task_id"
              placeholder="Enter task ID"
              :disabled="isLoading"
            />
          </UFormField>

          <UFormField name="assignee_id" label="Assignee ID">
            <UInput
              v-model="ticket.assignee_id"
              placeholder="Enter assignee ID"
              :disabled="isLoading"
            />
          </UFormField>

          <div class="form-actions">
            <UButton type="submit" color="primary" :loading="isLoading">
              Create Ticket
            </UButton>
          </div>
        </UForm>
      </div>
    </template>
  </UModal>
</template>

<script setup>
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
  task_id: '',
  assignee_id: ''
})

const statusOptions = [
  { label: 'Open', value: 'open' },
  { label: 'On Hold', value: 'on hold' },
  { label: 'Closed', value: 'closed' }
]

const resetForm = () => {
  ticket.value = {
    title: '',
    text: '',
    status: 'open',
    task_id: '',
    assignee_id: ''
  }
}

const handleSubmit = () => {
  const ticketData = {
    title: ticket.value.title || null,
    text: ticket.value.text || null,
    status: ticket.value.status || 'open',
    task_id: ticket.value.task_id || null,
    assignee_id: ticket.value.assignee_id || null,
    project_id: props.productionId || null,
    episode_id: props.episodeId || null
  }
  emit('submit', ticketData)
}

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
  border-top: 1px solid var(--color-gray-200);
}
</style>
