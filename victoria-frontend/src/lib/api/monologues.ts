import type { MonologueListItem, MonologueStatus } from "$lib/types/monologue";
import { MonologueListItem as MonologueListItemSchema } from "$lib/types/monologue";
import { Thought as ThoughtSchema } from "$lib/types/thought";
import type { Thought } from "$lib/types/thought";
import { URLSearchParams } from "happy-dom";
import { z } from "zod";

export async function getCurrentUserMonologues(
    triggerId: number | null = null,
    status: MonologueStatus | null = null,
    agentId: number | null = null,
    searchQuery: string | null = null
): Promise<MonologueListItem[]> {
    const params = new URLSearchParams();
    
    if (triggerId !== null) {
        params.append('trigger', triggerId);
    }
    
    if (status !== null) {
        params.append('monologueStatus', status);
    }
    
    if (agentId !== null) {
        params.append('assignedAgent', agentId);
    }
    
    if (searchQuery !== null) {
        params.append('searchQuery', searchQuery);
    }
    
    const res = await fetch(`/api/monologues?${params.toString()}`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(MonologueListItemSchema).parse(json);
}

export async function getMonologueThoughts(monologueId: number): Promise<Thought[]> {
    const res = await fetch(`/api/monologues/${monologueId}/thoughts`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(ThoughtSchema).parse(json);
}