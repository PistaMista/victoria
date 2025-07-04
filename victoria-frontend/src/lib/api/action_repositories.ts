import { ActionRepository as ActionRepositorySchema } from "$lib/types/action_repo";
import type { ActionRepository } from "$lib/types/action_repo";
import { z } from "zod";

export async function getActionRepositories(searchQuery: string | null = null): Promise<ActionRepository[]> {
    const params = new URLSearchParams();

    if (searchQuery) {
        params.append("searchQuery", searchQuery);
    }
    
    const res = await fetch(`/api/action-repos?${params.toString()}`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(ActionRepositorySchema).parse(json);
}