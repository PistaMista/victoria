import type { Trigger, TriggerListItem } from "$lib/types/trigger";
import { TriggerListItem as TriggerListItemSchema, Trigger as TriggerSchema } from "$lib/types/trigger";
import { z } from "zod"

export async function getPermittedTriggers(): Promise<TriggerListItem[]> {
    const res = await fetch('/api/triggers', {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(TriggerListItemSchema).parse(json);
}

export async function getAllTriggers(searchQuery: string | null = null): Promise<TriggerListItem[]> {
    let params = new URLSearchParams();

    if (searchQuery !== null) {
        params.append('searchQuery', searchQuery);
    }

    const res = await fetch(`/api/triggers/all?${params.toString()}`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(TriggerListItemSchema).parse(json);
}

export async function getTrigger(id: number): Promise<Trigger> {
    const res = await fetch(`/api/triggers/${id}`, {
        method: 'GET'
    });
    const json = await res.json();

    return TriggerSchema.parse(json);
}