import kitsuClient from 'kitsu-client-js'

let kitsuClientInstance = null

export const useKitsu = () => {
  const apiBaseUrl = '/api'

  if (!kitsuClientInstance) {
    console.log('Creating client', kitsuClient)
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
      return kitsuClientInstance.get('/plugins/tickets/tickets')
    },

    createTicket: (ticketData) => {
      return kitsuClientInstance.post('/plugins/tickets/tickets', ticketData)
    }

  }
}

