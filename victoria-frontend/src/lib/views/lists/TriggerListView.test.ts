import { expect, test, vi, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import TriggerListView from "./TriggerListView.svelte";
import { listTriggersHandler } from "../../../mocks/handlers/triggers";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("trigger list view contains all trigger names", async () => {
	const { container } = render(TriggerListView);

	await waitFor(() => {
		expect(container).toHaveTextContent("Generate recipes");
		expect(container).toHaveTextContent("Check news");
		expect(container).toHaveTextContent("General chat messages");
		expect(container).toHaveTextContent("Discord message received");
	});
});

test("trigger list view can search for triggers", async () => {
	const user = userEvent.setup();
	const { getByRole } = render(TriggerListView);

	const search = getByRole("search");
	await user.click(search);
	await user.keyboard("Discord");

	await waitFor(() => {
		expect(listTriggersHandler).toBeCalledTimes(2);
		expect(
			(listTriggersHandler as Mock).mock.calls[1][0].request.url,
		).toContain("searchQuery=Discord");
	});
});

test("clicking create button in trigger list view routes to trigger creation view", async () => {
	const user = userEvent.setup();
	const { getByLabelText } = render(TriggerListView);

	const createButton = getByLabelText("Create trigger");
	await user.click(createButton);

	expect(goto).toBeCalledWith("/admin/triggers/add");
});
