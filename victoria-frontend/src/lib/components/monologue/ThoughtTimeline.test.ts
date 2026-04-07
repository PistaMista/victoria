import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ThoughtTimeline from "./ThoughtTimeline.svelte";
import { connectWithRetry, disconnect } from "$lib/api/websocket";

test("thought timeline displays all text of the thoughts in a monologue", async () => {
	connectWithRetry();

	const { container } = render(ThoughtTimeline, {
		monologueId: 1,
	});

	await waitFor(() => {
		// Trigger
		expect(container).toHaveTextContent("An email has arrived...");

		// Verbatim
		expect(container).toHaveTextContent(
			"I should add the contained event to the calendar",
		);

		// Action
		expect(container).toHaveTextContent("web_search");
		expect(container).toHaveTextContent("top 10 restaurants in Brno");
		expect(container).toHaveTextContent("Some article title");

		// Success
		expect(container).toHaveTextContent("SUCCESS");
	});

	disconnect();
});
