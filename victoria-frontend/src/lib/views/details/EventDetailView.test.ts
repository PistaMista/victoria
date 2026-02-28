import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import EventDetailView from "./EventDetailView.svelte";

test("event detail shows event details", async () => {
	const { container } = render(EventDetailView, {
		id: 1,
	});

	await waitFor(() => {
		// Trigger name
		expect(container).toHaveTextContent("Generate recipes");
		// Event content
		expect(container).toHaveTextContent(
			"An email has arrived: 'Join the 2025 game access conference...'",
		);
	});
});
