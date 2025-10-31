import { Agent as AgentSchema, AgentListItem as AgentListItemSchema } from "$lib/types/agent";
import type { AgentListItem, Agent } from "$lib/types/agent";
import type { Diff } from "$lib/types/diff";
import type { MonologueListItem } from "$lib/types/monologue";
import { MonologueListItem as MonologueListItemSchema } from "$lib/types/monologue";
import { z } from "zod";

export async function getCurrentUserAgents(searchQuery: string | null = null): Promise<AgentListItem[]> {
	const params = new URLSearchParams();

	if (searchQuery) {
		params.append("searchQuery", searchQuery);
	}

	const res = await fetch(`/api/agents?${params.toString()}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(AgentListItemSchema).parse(json);
}

export async function getAgent(agentId: number): Promise<Agent> {
	const res = await fetch(`/api/agents/${agentId}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return AgentSchema.parse(json);
}

export async function getAgentMonologues(agentId: number): Promise<MonologueListItem[]> {
	const res = await fetch(`/api/agents/${agentId}/monologues`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(MonologueListItemSchema).parse(json);
}

export async function createAgent(agent: Agent): Promise<AgentListItem> {
	const res = await fetch('/api/agents', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(agent)
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return AgentListItemSchema.parse(json);
}

export async function updateAgent(id: number, changes: Diff<Agent>): Promise<boolean> {
	const res = await fetch(`/api/agents/${id}`, {
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

	return z.boolean().parse(json);
}

export async function deleteAgent(id: number): Promise<boolean> {
	const res = await fetch(`/api/agents/${id}`, {
		method: 'DELETE'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.boolean().parse(json);
}
