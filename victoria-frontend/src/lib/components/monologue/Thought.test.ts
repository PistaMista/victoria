import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import Component from "./Thought.svelte";
import type { Thought } from "$lib/types/thought";

test('thought bubble displays start time of given thought', async () => {
	const thought: Thought = {
		id: 1,
		startTimestamp: Date.UTC(2025, 4, 1, 11, 30) / 1000,
		invocation: {
			type: "ThoughtInvocation",
			name: null,
			parameters: {
				thought: "The user is sending a greeting"
			}
		},
		result: "The user is sending a greeting"
	};
	const { container } = render(Component, {
		thought: thought
	});

	expect(container).toHaveTextContent("2025/05/01 11:30")
})

test('action thought displays result of invocation and function name', async () => {
	const thought: Thought = {
		id: 2,
		startTimestamp: Date.UTC(2025, 5, 6, 11, 20) / 1000,
		invocation: {
			type: "ActionInvocation",
			name: "add_to_calendar",
			parameters: {}
		},
		result: "Failed to add event"
	};
	const { container } = render(Component, {
		thought: thought
	});

	expect(container).toHaveTextContent("add_to_calendar");
	expect(container).toHaveTextContent("Failed to add event");
})

test('trigger thought displays content of the triggering event as result and trigger name', async () => {
	const thought: Thought = {
		id: 2,
		startTimestamp: Date.UTC(2025, 5, 6, 11, 20) / 1000,
		invocation: {
			type: "TriggerInvocation",
			name: null,
			parameters: {
				eventId: 1
			}
		},
		result: "An email has arrived"
	};
	const { container } = render(Component, {
		thought: thought
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Generate recipes");
		expect(container).toHaveTextContent("An email has arrived");
	})
})

test('verbatim thought displays thought as result', async () => {
	const thought: Thought = {
		id: 2,
		startTimestamp: Date.UTC(2025, 5, 6, 11, 20) / 1000,
		invocation: {
			type: "ThoughtInvocation",
			name: null,
			parameters: {
				thought: "I should add the event to the calendar"
			}
		},
		result: "I should add the event to the calendar"
	};
	const { container } = render(Component, {
		thought: thought
	});

	expect(container).toHaveTextContent("I should add the event to the calendar");
})
