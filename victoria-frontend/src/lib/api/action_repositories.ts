import { ActionRepository as ActionRepositorySchema } from "$lib/types/action_repo";
import type { Diff } from "$lib/types/diff";
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
    
    if (!res.ok) {
        throw Error(json);
    }

    return z.array(ActionRepositorySchema).parse(json);
}

export async function getActionRepository(id: number): Promise<ActionRepository> {
    const res = await fetch(`/api/action-repos/${id}`, {
        method: 'GET'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return ActionRepositorySchema.parse(json);
}

export async function updateActionRepository(id: number, changes: Diff<ActionRepository>): Promise<Boolean> {
    const res = await fetch(`/api/action-repos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(changes)
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return z.boolean().parse(json);
}

export async function deleteActionRepository(id: number): Promise<Boolean> {
    const res = await fetch(`/api/action-repos/${id}`, {
        method: 'DELETE'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return z.boolean().parse(json);
}

export async function createActionRepository(newRepo: ActionRepository): Promise<ActionRepository> {
    const res = await fetch(`/api/action-repos`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newRepo)
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return ActionRepositorySchema.parse(json);
}