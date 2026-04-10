import kitsuClient from "kitsu-client-js"

let kitsuClientInstance = null

export const useKitsu = () => {
  const apiBaseUrl = "/api"

  if (!kitsuClientInstance) {
    kitsuClientInstance = kitsuClient.createClient(apiBaseUrl)
  }

  return {
    client: kitsuClientInstance,

    getOpenProductions: () => {
      return kitsuClientInstance.getOpenProductions()
    },

    getProject: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}`)
    },

    getPeople: () => {
      return kitsuClientInstance.get("/data/persons")
    },

    getAssetTypes: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/asset-types`)
    },

    getAssets: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/assets`)
    },

    getShots: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/shots`)
    },

    getSequences: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/sequences`)
    },

    getEpisodes: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/episodes`)
    },

    getEdits: (projectId) => {
      return kitsuClientInstance.get(`/data/projects/${projectId}/edits`)
    },

    getTaskTypes: (projectId) => {
      return kitsuClientInstance.get(
        projectId
          ? `/data/projects/${projectId}/task-types`
          : "/data/task-types"
      )
    },

    getTasksForEntity: (entityId) => {
      return kitsuClientInstance.get(`/data/tasks?entity_id=${entityId}`)
    },

    getTask: (taskId) => {
      return kitsuClientInstance.get(`/data/tasks/${taskId}`)
    },

    fetchTickets: (productionId, episodeId) => {
      const query = {}
      if (productionId) {
        query.production_id = productionId
      }
      if (episodeId) {
        query.episode_id = episodeId
      }
      return kitsuClientInstance.get("/plugins/tickets/tickets", { query })
    },

    createTicket: (ticketData) => {
      return kitsuClientInstance.post("/plugins/tickets/tickets", ticketData)
    },

    updateTicket: (ticketId, ticketData) => {
      return kitsuClientInstance.put(
        `/plugins/tickets/tickets/${ticketId}`,
        ticketData
      )
    },

    deleteTicket: (ticketId) => {
      return kitsuClientInstance.delete(
        `/plugins/tickets/tickets/${ticketId}`
      )
    }
  }
}
