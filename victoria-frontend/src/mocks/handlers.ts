import { http, HttpResponse } from "msw"

export const handlers = [
    /// THESE ENDPOINTS ALWAYS WORK ON OBJECTS OWNED
    /// BY THE CURRENTLY SIGNED IN USER
    /* CHATS */
    http.get('/api/chats', () => {}),
    http.post('/api/chats', () => {}),
    http.delete('/api/chats/:id', () => {}),

    http.get('/api/chats/:id/exchanges', () => {}),
    // This returns the ID of the created exchange
    http.post('/api/chats/:id/send-message', () => {}),

    http.get('/api/chats/:id/options', () => {}),
    http.put('/api/chats/:id/options', () => {}),
    
    /* EXCHANGES */
    http.get('/api/exchanges/:id', () => {}),
    http.get('/api/exchanges/:id/messages', () => {}),
    // This is an HTTP long poll for new messages
    http.get('/api/exchanges/:id/messages/new', () => {}),
    
    /* MESSAGES */
    http.get('/api/messages/:id', () => {}),
    
    /* AGENTS */
    http.get('/api/agents', () => {}),
    http.post('/api/agents', () => {}),
    
    http.get('/api/agents/:id', () => {}),
    http.put('/api/agents/:id', () => {}),
    http.delete('/api/agents/:id', () => {}),

    http.get('/api/agents/:id/monologues', () => {}),
    
    /* MONOLOGUES */
    http.get('/api/monologues', () => {}),
    http.get('/api/monologues/:id', () => {}),
    
    http.get('/api/monologues/:id/thoughts', () => {}),

    /* EVENTS */
    http.get('/api/events/:id', () => {}),

    /* THOUGHTS */
    http.get('/api/thoughts/:id', () => {}),
    
    /// POST, PUT AND DELETE ENDPOINTS BELOW REQUIRE ADMIN ROLE
    /* USERS */
    http.get('/api/users', () => {}),
    http.post('/api/users', () => {}),
    
    http.get('/api/users/:id', () => {}),
    http.put('/api/users/:id', () => {}),
    http.delete('/api/users/:id', () => {}),

    /* ACTION REPOSITORIES */
    http.get('/api/action-repos', () => {}),
    http.post('/api/action-repos', () => {}),
    
    http.get('/api/action-repos/:id', () => {}),
    http.put('/api/action-repos/:id', () => {}),
    http.delete('/api/action-repos/:id', () => {}),
    
    /* CONNECTIONS */
    http.get('/api/connections', () => {}),
    http.post('/api/connections', () => {}),

    http.get('/api/connections/:id', () => {}),
    http.put('/api/connections/:id', () => {}),
    http.delete('/api/connections/:id', () => {}),

    /* TRIGGERS */
    http.get('/api/triggers', () => {}),
    http.post('/api/triggers', () => {}),

    http.get('/api/triggers/:id', () => {}),
    http.put('/api/triggers/:id', () => {}),
    http.delete('/api/triggers/:id', () => {}),

    /* MODELS */
    http.get('/api/models', () => {}),
    http.post('/api/models/:id/enable', () => {}),
    http.post('/api/models/:id/disable', () => {}),
    
    /// BELOW ARE ENDPOINTS FOR INTEGRATION WITH EXTERNAL SERVICES    
    http.post('/api/webhook/:url', () => {}),
]