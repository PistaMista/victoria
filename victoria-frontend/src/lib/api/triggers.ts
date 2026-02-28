import type { Diff } from "$lib/types/diff";
import type { Trigger, TriggerListItem } from "$lib/types/trigger";
import {
	TriggerListItem as TriggerListItemSchema,
	Trigger as TriggerSchema,
} from "$lib/types/trigger";
import { z } from "zod";

export async function getPermittedTriggers(): Promise<TriggerListItem[]> {
	const res = await fetch("/api/triggers", {
		method: "GET",
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(TriggerListItemSchema).parse(json);
}

export async function getAllTriggers(
	searchQuery: string | null = null,
): Promise<TriggerListItem[]> {
	let params = new URLSearchParams();

	if (searchQuery !== null) {
		params.append("searchQuery", searchQuery);
	}

	const res = await fetch(`/api/triggers/all?${params.toString()}`, {
		method: "GET",
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(TriggerListItemSchema).parse(json);
}

export async function getTrigger(id: number): Promise<Trigger> {
	const res = await fetch(`/api/triggers/${id}`, {
		method: "GET",
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return TriggerSchema.parse(json);
}

export async function updateTrigger(
	id: number,
	changes: Diff<Trigger>,
): Promise<void> {
	const res = await fetch(`/api/triggers/${id}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(changes),
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function deleteTrigger(id: number): Promise<void> {
	const res = await fetch(`/api/triggers/${id}`, {
		method: "DELETE",
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function createTrigger(
	trigger: Trigger,
): Promise<TriggerListItem> {
	const res = await fetch("/api/triggers", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(trigger),
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return TriggerListItemSchema.parse(json);
}
