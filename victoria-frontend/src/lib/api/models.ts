import { z } from "zod"
import type { Model } from "$lib/types/model"
import { Model as ModelSchema } from "$lib/types/model"

export async function getEnabledModels(): Promise<Model[]> {
    const res = await fetch('/api/models/enabled', {
        method: 'GET'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return z.array(ModelSchema).parse(json);
}

export async function getAllModels(): Promise<Model[]> {
    const res = await fetch('/api/models/all', {
        method: 'GET'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return z.array(ModelSchema).parse(json);
}

export async function setModelEnabled(id: number, enabled: boolean): Promise<Boolean> {
    const res = await fetch(`/api/models/${id}/${enabled? "enable" : "disable"}`, {
        method: 'POST'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }

    return z.boolean().parse(json);
}