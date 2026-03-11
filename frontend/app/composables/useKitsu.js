import kitsuClient from "kitsu-client-js"

let kitsuClientInstance = null

export const useKitsu = () => {
  const apiBaseUrl = "/api"

  if (!kitsuClientInstance) {
    kitsuClientInstance = kitsuClient.createClient(apiBaseUrl)
  }

  return {
    client: kitsuClientInstance,

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
