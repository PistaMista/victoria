import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ModelSettingsDetailView from "./ModelSettingsDetailView.svelte";

test("model settings detail view lists all imported model names", async () => {
	const { container } = render(ModelSettingsDetailView);

	await waitFor(() => {
		expect(container).toHaveTextContent("gemma3:12b");
		expect(container).toHaveTextContent("llama3.1:8b");
	});
});

// Rest is covered by tests for ModelToggle
