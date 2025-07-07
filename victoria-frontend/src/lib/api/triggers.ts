import type { TriggerListItem } from "$lib/types/trigger";
import { TriggerListItem as TriggerListItemSchema } from "$lib/types/trigger";
import { z } from "zod"

export async function getPermittedTriggers(): Promise<TriggerListItem[]> {
    const res = await fetch('/api/triggers', {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(TriggerListItemSchema).parse(json);
}
