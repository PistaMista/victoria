import { ConnectionListItem, type Connection } from "$lib/types/connection";
import { Connection as ConnectionSchema, ConnectionListItem as ConnectionListItemSchema } from "$lib/types/connection";
import type { Diff } from "$lib/types/diff";
import { z } from "zod";


export async function listConnections(): Promise<ConnectionListItem[]> {
	const res = await fetch(`/api/connections`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(ConnectionListItemSchema).parse(json);
}

export async function getConnection(id: number): Promise<Connection> {
	const res = await fetch(`/api/connections/${id}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return ConnectionSchema.parse(json);
}

export async function updateConnection(id: number, changes: Diff<Connection>): Promise<void> {
	const res = await fetch(`/api/connections/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(changes)
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function deleteConnection(id: number): Promise<void> {
	const res = await fetch(`/api/connections/${id}`, {
		method: 'DELETE'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function createConnection(newConnection: Connection): Promise<ConnectionListItem> {
	const res = await fetch(`/api/connections`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(newConnection)
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return ConnectionListItem.parse(json);
}
