import type { Action } from "$lib/types/action";
import { Action as ActionSchema } from "$lib/types/action";
import { z } from "zod"

export async function getPermittedActions(): Promise<Action[]> {
	const res = await fetch('/api/actions', {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(ActionSchema).parse(json);
}

export async function getAllActions(): Promise<Action[]> {
	const res = await fetch('/api/actions/all', {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(ActionSchema).parse(json);
}
