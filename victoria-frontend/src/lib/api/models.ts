import { z } from "zod"
import type { Model } from "$lib/types/model"
import { Model as ModelSchema } from "$lib/types/model"

export async function getEnabledModels(): Promise<Model[]> {
    const res = await fetch('/api/models', {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(ModelSchema).parse(json);
}

export async function setModelEnabled(id: number, enabled: boolean): Promise<Boolean> {
    const res = await fetch(`/api/models/${id}/${enabled? "enable" : "disable"}`, {
        method: 'POST'
    });
    const json = await res.json();

    return z.boolean().parse(json);
}