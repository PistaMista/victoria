import type { Monologue, MonologueListItem, MonologueStatus } from "$lib/types/monologue";
import { MonologueListItem as MonologueListItemSchema, Monologue as MonologueSchema } from "$lib/types/monologue";
import { Thought as ThoughtSchema } from "$lib/types/thought";
import type { Thought } from "$lib/types/thought";
import { z } from "zod";

export async function getCurrentUserMonologues(
	triggerId: number | null = null,
	status: MonologueStatus | null = null,
	agentId: number | null = null,
	searchQuery: string | null = null
): Promise<MonologueListItem[]> {
	const params = new URLSearchParams();

	if (triggerId !== null) {
		params.append('trigger', triggerId.toString());
	}

	if (status !== null) {
		params.append('monologueStatus', status);
	}

	if (agentId !== null) {
		params.append('assignedAgent', agentId.toString());
	}

	if (searchQuery !== null) {
		params.append('searchQuery', searchQuery);
	}

	const res = await fetch(`/api/monologues?${params.toString()}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(MonologueListItemSchema).parse(json);
}

export async function getMonologue(id: number): Promise<Monologue> {
	const res = await fetch(`/api/monologues/${id}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return MonologueSchema.parse(json);
}

export async function getMonologueThoughts(monologueId: number): Promise<Thought[]> {
	const res = await fetch(`/api/monologues/${monologueId}/thoughts`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(ThoughtSchema).parse(json);
}

export async function abortMonologue(id: number): Promise<boolean> {
	const res = await fetch(`/api/monologues/${id}/abort`, {
		method: 'POST'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.boolean().parse(json);
}
