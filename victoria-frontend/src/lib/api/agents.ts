import { AgentListItem } from "$lib/types/agent";
import type { MonologueListItem } from "$lib/types/monologue";
import { MonologueListItem as MonologueListItemSchema } from "$lib/types/monologue";
import { z } from "zod";

export async function getCurrentUserAgents(searchQuery: string | null): Promise<AgentListItem[]> {
    const params = new URLSearchParams();

    if (searchQuery) {
        params.append("searchQuery", searchQuery);
    }

    const res = await fetch(`/api/agents?${params.toString()}`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(AgentListItem).parse(json);
}

export async function getAgentMonologues(agentId: number): Promise<MonologueListItem[]> {
    const res = await fetch(`/api/agents/${agentId}/monologues`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(MonologueListItemSchema).parse(json);
}