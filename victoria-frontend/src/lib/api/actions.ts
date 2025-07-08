import type { Action } from "$lib/types/action";
import { Action as ActionSchema } from "$lib/types/action";
import { z } from "zod"

export async function getPermittedActions(): Promise<Action[]> {
    const res = await fetch('/api/actions', {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(ActionSchema).parse(json);
}