import { delay, http, HttpResponse } from "msw";
import { Monologue, MonologueListItem } from "$lib/types/monologue";
import { Thought } from "$lib/types/thought";
import { spy } from "../spy";

export const listMonologuesHandler = await spy(() => {
	return HttpResponse.json<Array<MonologueListItem>>([
		{
			id: 1,
			agentId: 2,
			status: "RUNNING",
			startTimestamp: 3000,
			title: "Research thesis ideas",
			summary: "Searching the web for sources",
		},
		{
			id: 2,
			agentId: 1,
			status: "SUCCESS",
			startTimestamp: 2000,
			title: "Generate recipes for the week",
			summary: "Checking available ingredients",
		},
	]);
});

export const getMonologueHandler = await spy(({ params: { id } }) => {
	switch (id) {
		case "1":
			return HttpResponse.json<Monologue>({
				id: 1,
				agentId: 2,
				startTimestamp: 3000,
				endTimestamp: 3000,
				status: "RUNNING",
				title: "Research thesis ideas",
				summary: "Searching the web for sources",
			});
		case "2":
			return HttpResponse.json<Monologue>({
				id: 2,
				agentId: 1,
				startTimestamp: 3000,
				endTimestamp: 3000,
				status: "SUCCESS",
				title: "Generate recipes for the week",
				summary: "Checking available ingredients",
			});
	}
});

export const socketSendMonologueStatus = await spy(async (client: any, handlerId: number, monologueId: number) => {
	switch (monologueId) {
		case 1:
			client.send(JSON.stringify({
				type: "eventMessage",
				handlerIds: [handlerId],
				content: {
					monologue: {
						id: 1,
						agentId: 2,
						startTimestamp: 3000,
						endTimestamp: 3000,
						status: "PENDING",
						title: "Untitled",
						summary: "Searching the web for sources",
					}
				}
			}));

			await delay(100);

			client.send(JSON.stringify({
				type: "eventMessage",
				handlerIds: [handlerId],
				content: {
					monologue: {
						id: 1,
						agentId: 2,
						startTimestamp: 3000,
						endTimestamp: 3000,
						status: "RUNNING",
						title: "Research thesis ideas",
						summary: "Searching the web for sources",
					}
				}
			}));
			break;
		case 2:
			client.send(JSON.stringify({
				type: "eventMessage",
				handlerIds: [handlerId],
				content: {
					monologue: {
						id: 2,
						agentId: 1,
						startTimestamp: 3000,
						endTimestamp: 3000,
						status: "SUCCESS",
						title: "Generate recipes for the week",
						summary: "Checking available ingredients",
					}
				}
			}));
			break;
	}
});

export const abortMonologueHandler = await spy(() => {
	return HttpResponse.json<boolean>(true);
});

export const getMonologueThoughtsHandler = await spy(() => {
	return HttpResponse.json<Array<Thought>>([
		{
			id: 1,
			startTimestamp: Date.UTC(2026, 1, 20, 20, 22),
			invocation: {
				type: "TriggerInvocation",
				name: null,
				parameters: {
					eventId: 1,
				},
			},
			/// This is the content of the triggering event
			result: "An email has arrived...",
		},
		{
			id: 2,
			startTimestamp: Date.UTC(2026, 1, 20, 20, 22),
			invocation: {
				type: "ThoughtInvocation",
				name: null,
				parameters: {
					thought: "I should add the contained event to the calendar",
				},
			},
			result: "I should add the contained event to the calendar",
		},
		{
			id: 3,
			startTimestamp: Date.UTC(2026, 1, 20, 20, 22),
			invocation: {
				type: "ActionInvocation",
				name: "web_search",
				parameters: {
					query: "top 10 restaurants in Brno",
				},
			},
			result: "[ { title: 'Some article title', summary: 'Some summary' } ]",
		},
		{
			id: 4,
			startTimestamp: Date.UTC(2026, 1, 20, 20, 22),
			invocation: {
				type: "SuccessInvocation",
				name: null,
				parameters: {},
			},
			result: "",
		},
	]);
});

export const handlers = [
	http.get("/api/monologues", listMonologuesHandler),
	http.get("/api/monologues/:id", getMonologueHandler),

	http.post("/api/monologues/:id/abort", abortMonologueHandler),
	http.get("/api/monologues/:id/thoughts", getMonologueThoughtsHandler),
];
