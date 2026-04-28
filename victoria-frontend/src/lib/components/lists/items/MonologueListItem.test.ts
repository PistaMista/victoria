import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import type { MonologueListItem as Monologue } from "$lib/types/monologue";
import MonologueListItem from "./MonologueListItem.svelte";
import { goto } from "$app/navigation";
import { connectWithRetry, disconnect } from "$lib/api/websocket";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

const testMonologue: Monologue = {
	id: 2,
	agentId: 1,
	startTimestamp: 3000,
	title: "Research reading list for learning electronics",
	summary: "Thinking...",
	status: "PENDING",
};

test("monologue list item shows title of given monologue", async () => {
	const { container } = render(MonologueListItem, {
		monologue: testMonologue,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent(
			"Research reading list for learning electronics",
		);
	});
});

test("monologue list item shows summary of given monologue", async () => {
	const { container } = render(MonologueListItem, {
		monologue: testMonologue,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Thinking...");
	});
});

test("monologue list item replaces summary of given monologue after change", async () => {
	let testMonologue2 = { ...testMonologue, id: 1 };

	const { container } = render(MonologueListItem, {
		monologue: testMonologue2,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Searching the web for sources");
	});
});

test("clicking monologue list item routes to given monologue detail view", async () => {
	const user = userEvent.setup();
	const { getByRole } = render(MonologueListItem, {
		monologue: testMonologue,
	});
	const button = getByRole("button");

	await user.click(button);

	expect(goto).toBeCalledWith("/monologues/2");
});
