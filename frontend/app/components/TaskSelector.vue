<template>
  <div class="task-selector">
    <p v-if="!projectId" class="task-selector-hint">
      {{ $t('tickets.create.select_project_first') }}
    </p>

    <template v-else-if="project">
      <!-- Entity type -->
      <USelectMenu
        v-model="selectedEntityType"
        :items="entityTypeOptions"
        value-key="value"
        :placeholder="$t('tickets.create.entity_type_placeholder')"
        :disabled="disabled"
        :loading="isLoadingProject"
        class="w-full"
      />

      <!-- ASSET path -->
      <template v-if="val(selectedEntityType) === 'Asset'">
        <USelectMenu
          v-model="selectedAssetTypeId"
          :items="assetTypeOptions"
          value-key="value"
          :placeholder="$t('tickets.create.asset_type_placeholder')"
          :disabled="disabled"
          :loading="isLoadingOptions"
          class="w-full"
        />
        <USelectMenu
          v-if="val(selectedAssetTypeId)"
          v-model="selectedEntityId"
          :items="filteredAssetOptions"
          value-key="value"
          :placeholder="$t('tickets.create.entity_placeholder')"
          :disabled="disabled"
          class="w-full"
        />
      </template>

      <!-- SHOT path -->
      <template v-if="val(selectedEntityType) === 'Shot'">
        <USelectMenu
          v-if="isTvShow"
          v-model="selectedEpisodeId"
          :items="episodeOptions"
          value-key="value"
          :placeholder="$t('tickets.create.episode_placeholder')"
          :disabled="disabled"
          :loading="isLoadingOptions"
          class="w-full"
        />
        <USelectMenu
          v-if="!isTvShow || val(selectedEpisodeId)"
          v-model="selectedSequenceId"
          :items="filteredSequenceOptions"
          value-key="value"
          :placeholder="$t('tickets.create.sequence_placeholder')"
          :disabled="disabled"
          class="w-full"
        />
        <USelectMenu
          v-if="val(selectedSequenceId)"
          v-model="selectedEntityId"
          :items="filteredShotOptions"
          value-key="value"
          :placeholder="$t('tickets.create.entity_placeholder')"
          :disabled="disabled"
          class="w-full"
        />
      </template>

      <!-- SEQUENCE path -->
      <template v-if="val(selectedEntityType) === 'Sequence'">
        <USelectMenu
          v-if="isTvShow"
          v-model="selectedEpisodeId"
          :items="episodeOptions"
          value-key="value"
          :placeholder="$t('tickets.create.episode_placeholder')"
          :disabled="disabled"
          :loading="isLoadingOptions"
          class="w-full"
        />
        <USelectMenu
          v-if="!isTvShow || val(selectedEpisodeId)"
          v-model="selectedEntityId"
          :items="filteredSequenceOptions"
          value-key="value"
          :placeholder="$t('tickets.create.entity_placeholder')"
          :disabled="disabled"
          class="w-full"
        />
      </template>

      <!-- EPISODE path (tvshow only) -->
      <template v-if="val(selectedEntityType) === 'Episode'">
        <USelectMenu
          v-model="selectedEntityId"
          :items="episodeOptions"
          value-key="value"
          :placeholder="$t('tickets.create.episode_placeholder')"
          :disabled="disabled"
          :loading="isLoadingOptions"
          class="w-full"
        />
      </template>

      <!-- EDIT path -->
      <template v-if="val(selectedEntityType) === 'Edit'">
        <USelectMenu
          v-if="isTvShow"
          v-model="selectedEpisodeId"
          :items="episodeOptions"
          value-key="value"
          :placeholder="$t('tickets.create.episode_placeholder')"
          :disabled="disabled"
          :loading="isLoadingOptions"
          class="w-full"
        />
        <USelectMenu
          v-if="!isTvShow || val(selectedEpisodeId)"
          v-model="selectedEntityId"
          :items="filteredEditOptions"
          value-key="value"
          :placeholder="$t('tickets.create.entity_placeholder')"
          :disabled="disabled"
          class="w-full"
        />
      </template>

      <!-- TASK (final step) -->
      <USelectMenu
        v-if="val(selectedEntityId)"
        v-model="selectedTaskId"
        :items="taskOptions"
        value-key="value"
        :placeholder="$t('tickets.create.task_placeholder')"
        :disabled="disabled"
        :loading="isLoadingTasks"
        class="w-full"
      />
    </template>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const {
  getProject, getAssetTypes, getAssets, getShots,
  getSequences, getEpisodes, getEdits,
  getTaskTypes, getTasksForEntity, getTask
} = useKitsu()

const props = defineProps({
  projectId: { type: String, default: null },
  taskId: { type: String, default: null },
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['update:taskId'])

// USelectMenu may return the full item object or just the value string
// depending on Nuxt UI version. This helper normalizes to a string.
const val = (v) => {
  if (!v) return null
  if (typeof v === 'object') return v.value || v.id || null
  return v
}

// Data
const project = ref(null)
const taskTypeMap = ref({})
const assetTypes = ref([])
const assets = ref([])
const shots = ref([])
const sequences = ref([])
const episodes = ref([])
const edits = ref([])
const tasks = ref([])

// Selection state
const selectedEntityType = ref(null)
const selectedAssetTypeId = ref(null)
const selectedEpisodeId = ref(null)
const selectedSequenceId = ref(null)
const selectedEntityId = ref(null)
const selectedTaskId = ref(null)

// Loading
const isLoadingProject = ref(false)
const isLoadingOptions = ref(false)
const isLoadingTasks = ref(false)
const isInitializing = ref(false)

// Computed
const isTvShow = computed(() => project.value?.production_type === 'tvshow')

const entityTypeOptions = computed(() => {
  const options = [
    { label: t('tickets.create.asset'), value: 'Asset' },
    { label: t('tickets.create.shot'), value: 'Shot' },
    { label: t('tickets.create.sequence'), value: 'Sequence' },
    { label: t('tickets.create.edit'), value: 'Edit' }
  ]
  if (isTvShow.value) {
    options.splice(3, 0, { label: t('tickets.create.episode'), value: 'Episode' })
  }
  return options
})

const assetTypeOptions = computed(() =>
  assetTypes.value.map((at) => ({ label: at.name, value: at.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
)

const episodeOptions = computed(() =>
  episodes.value.map((e) => ({ label: e.name, value: e.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
)

const filteredSequenceOptions = computed(() => {
  let list = sequences.value
  const epId = val(selectedEpisodeId.value)
  if (isTvShow.value && epId) {
    list = list.filter((s) => s.parent_id === epId)
  }
  return list.map((s) => ({ label: s.name, value: s.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const filteredAssetOptions = computed(() => {
  let list = assets.value
  const atId = val(selectedAssetTypeId.value)
  if (atId) {
    list = list.filter((a) => a.entity_type_id === atId)
  }
  return list.map((a) => ({ label: a.name, value: a.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const filteredShotOptions = computed(() => {
  let list = shots.value
  const seqId = val(selectedSequenceId.value)
  if (seqId) {
    list = list.filter((s) => s.sequence_id === seqId || s.parent_id === seqId)
  }
  return list.map((s) => ({ label: s.name, value: s.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const filteredEditOptions = computed(() => {
  let list = edits.value
  const epId = val(selectedEpisodeId.value)
  if (isTvShow.value && epId) {
    list = list.filter((e) => e.episode_id === epId || e.parent_id === epId)
  }
  return list.map((e) => ({ label: e.name, value: e.id }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const getTaskTypeName = (task) => {
  if (task.task_type_name) return task.task_type_name
  if (task.task_type && task.task_type.name) return task.task_type.name
  if (taskTypeMap.value[task.task_type_id]) return taskTypeMap.value[task.task_type_id]
  return task.task_type_id
}

const taskOptions = computed(() =>
  tasks.value.map((task) => ({
    label: getTaskTypeName(task),
    value: task.id
  }))
)

// Reset helpers
const resetAll = () => {
  selectedEntityType.value = null
  selectedAssetTypeId.value = null
  selectedEpisodeId.value = null
  selectedSequenceId.value = null
  selectedEntityId.value = null
  selectedTaskId.value = null
  assetTypes.value = []
  assets.value = []
  shots.value = []
  sequences.value = []
  episodes.value = []
  edits.value = []
  tasks.value = []
}

const resetBelow = (level) => {
  if (level <= 1) { selectedAssetTypeId.value = null; selectedEpisodeId.value = null }
  if (level <= 2) { selectedSequenceId.value = null }
  if (level <= 3) { selectedEntityId.value = null }
  if (level <= 4) { selectedTaskId.value = null; tasks.value = [] }
}

// Fetch entity lists based on entity type
const fetchEntityData = async (entityType) => {
  if (!props.projectId) return
  isLoadingOptions.value = true
  try {
    const fetches = []
    if (entityType === 'Asset') {
      fetches.push(
        getAssetTypes(props.projectId).then((d) => { assetTypes.value = d }),
        getAssets(props.projectId).then((d) => { assets.value = d })
      )
    } else if (entityType === 'Shot') {
      if (isTvShow.value) {
        fetches.push(getEpisodes(props.projectId).then((d) => { episodes.value = d }))
      }
      fetches.push(
        getSequences(props.projectId).then((d) => { sequences.value = d }),
        getShots(props.projectId).then((d) => { shots.value = d })
      )
    } else if (entityType === 'Sequence') {
      if (isTvShow.value) {
        fetches.push(getEpisodes(props.projectId).then((d) => { episodes.value = d }))
      }
      fetches.push(getSequences(props.projectId).then((d) => { sequences.value = d }))
    } else if (entityType === 'Episode') {
      fetches.push(getEpisodes(props.projectId).then((d) => { episodes.value = d }))
    } else if (entityType === 'Edit') {
      if (isTvShow.value) {
        fetches.push(getEpisodes(props.projectId).then((d) => { episodes.value = d }))
      }
      fetches.push(getEdits(props.projectId).then((d) => { edits.value = d }))
    }
    await Promise.all(fetches)
  } catch (error) {
    console.error('Error fetching entity data:', error)
  } finally {
    isLoadingOptions.value = false
  }
}

// Initialize from existing task_id (edit mode)
// Walk up the parent hierarchy to rebuild the full selection path
const initializeFromTaskId = async (taskId) => {
  if (!taskId || !props.projectId) return
  try {
    const task = await getTask(taskId)
    const entityId = task.entity_id

    const [assetTypesData, assetsData, shotsData, sequencesData, episodesData, editsData] =
      await Promise.all([
        getAssetTypes(props.projectId),
        getAssets(props.projectId),
        getShots(props.projectId),
        getSequences(props.projectId),
        getEpisodes(props.projectId),
        getEdits(props.projectId)
      ])

    assetTypes.value = assetTypesData
    assets.value = assetsData
    shots.value = shotsData
    sequences.value = sequencesData
    episodes.value = episodesData
    edits.value = editsData

    const asset = assetsData.find((a) => a.id === entityId)
    const shot = shotsData.find((s) => s.id === entityId)
    const sequence = sequencesData.find((s) => s.id === entityId)
    const episode = episodesData.find((e) => e.id === entityId)
    const edit = editsData.find((e) => e.id === entityId)

    if (asset) {
      selectedEntityType.value = 'Asset'
      selectedAssetTypeId.value = asset.entity_type_id
      selectedEntityId.value = asset.id
    } else if (shot) {
      selectedEntityType.value = 'Shot'
      // Walk up: shot → sequence (parent_id) → episode (sequence.parent_id)
      const parentSequence = sequencesData.find(
        (s) => s.id === (shot.sequence_id || shot.parent_id)
      )
      if (isTvShow.value && parentSequence) {
        selectedEpisodeId.value = parentSequence.parent_id
      }
      selectedSequenceId.value = shot.sequence_id || shot.parent_id
      selectedEntityId.value = shot.id
    } else if (sequence) {
      selectedEntityType.value = 'Sequence'
      if (isTvShow.value) {
        selectedEpisodeId.value = sequence.parent_id
      }
      selectedEntityId.value = sequence.id
    } else if (episode) {
      selectedEntityType.value = 'Episode'
      selectedEntityId.value = episode.id
    } else if (edit) {
      selectedEntityType.value = 'Edit'
      if (isTvShow.value) {
        // Walk up: edit → episode (parent_id)
        selectedEpisodeId.value = edit.episode_id || edit.parent_id
      }
      selectedEntityId.value = edit.id
    }

    tasks.value = await getTasksForEntity(entityId)
    selectedTaskId.value = taskId
  } catch (error) {
    console.error('Error initializing from task:', error)
  }
}

// Watchers
watch(() => props.projectId, async (newId) => {
  isInitializing.value = true
  resetAll()
  project.value = null
  taskTypeMap.value = {}
  if (!newId) {
    isInitializing.value = false
    emit('update:taskId', null)
    return
  }
  isLoadingProject.value = true
  try {
    project.value = await getProject(newId)
  } catch (error) {
    console.error('Error fetching project:', error)
  }
  try {
    const taskTypesData = await getTaskTypes(newId)
    const map = {}
    if (Array.isArray(taskTypesData)) {
      for (const tt of taskTypesData) {
        map[tt.id] = tt.name
      }
    }
    taskTypeMap.value = map
  } catch (error) {
    console.error('Error fetching task types:', error)
  }
  if (props.taskId && project.value) {
    await initializeFromTaskId(props.taskId)
  }
  isInitializing.value = false
  isLoadingProject.value = false
  emit('update:taskId', val(selectedTaskId.value) || null)
}, { immediate: true })

watch(selectedEntityType, (newType) => {
  if (isInitializing.value) return
  resetBelow(1)
  if (val(newType)) fetchEntityData(val(newType))
})

watch(selectedAssetTypeId, () => {
  if (isInitializing.value) return
  resetBelow(3)
})

watch(selectedEpisodeId, () => {
  if (isInitializing.value) return
  resetBelow(2)
})

watch(selectedSequenceId, () => {
  if (isInitializing.value) return
  resetBelow(3)
})

watch(selectedEntityId, async (newId) => {
  if (isInitializing.value) return
  selectedTaskId.value = null
  tasks.value = []
  const id = val(newId)
  if (!id) return
  isLoadingTasks.value = true
  try {
    tasks.value = await getTasksForEntity(id)
  } catch (error) {
    console.error('Error fetching tasks:', error)
  } finally {
    isLoadingTasks.value = false
  }
})

watch(selectedTaskId, (newId) => {
  if (isInitializing.value) return
  emit('update:taskId', val(newId) || null)
})
</script>

<style scoped>
.task-selector {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-selector-hint {
  color: var(--text-muted);
  font-size: 0.875rem;
  margin: 0;
}
</style>
