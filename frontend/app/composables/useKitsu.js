import kitsuClient from "kitsu-client-js"

let kitsuClientInstance = null

export const useKitsu = () => {
  const apiBaseUrl = "/api"

  if (!kitsuClientInstance) {
    console.log("Creating client", kitsuClient)
    kitsuClientInstance = kitsuClient.createClient(apiBaseUrl)
  }

  return {
    client: kitsuClientInstance,

    context: (email, password) => {
      return kitsuClientInstance.context(email, password)
    },
    getOpenProductions: () => {
      return kitsuClientInstance.getOpenProductions()
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

    deleteTicket: (ticketId) => {
      return kitsuClientInstance.delete(`/plugins/tickets/tickets/${ticketId}`)
    },

    getAssetTypes: (projectId) => {
      return kitsuClientInstance.get(
        `/api/data/projects/${projectId}/asset-types`,
      )
    },

    getAssets: (projectId) => {
      return kitsuClientInstance.get(`/api/data/projects/${projectId}/assets`)
    },
  }
}
