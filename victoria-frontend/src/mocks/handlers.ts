import { handlers as chats } from "./handlers/chats"
import { handlers as exchanges } from "./handlers/exchanges"
import { handlers as agents } from "./handlers/agents"
import { handlers as monologues } from "./handlers/monologues"
import { handlers as events } from "./handlers/events"
import { handlers as users } from "./handlers/users"
import { handlers as action_repos } from "./handlers/action_repos"
import { handlers as actions } from "./handlers/actions"
import { handlers as connections } from "./handlers/connections"
import { handlers as triggers } from "./handlers/triggers"
import { handlers as models } from "./handlers/models"


export const handlers = [
    /// THESE ENDPOINTS ALWAYS WORK ON OBJECTS OWNED
    /// BY THE CURRENTLY SIGNED IN USER
    /* CHATS */
    ...chats,
    /* EXCHANGES */
    ...exchanges,
    /* AGENTS */
    ...agents,
    /* MONOLOGUES */
    ...monologues,
    /* EVENTS */
    ...events,
    /// POST, PUT AND DELETE ENDPOINTS BELOW REQUIRE ADMIN ROLE
    /* USERS */
    ...users,
    /* ACTION REPOSITORIES */
    ...action_repos,
    /* ACTIONS */
    ...actions,
    /* CONNECTIONS */
    ...connections,
    /* TRIGGERS */
    ...triggers,
    /* MODELS */
    ...models,
]