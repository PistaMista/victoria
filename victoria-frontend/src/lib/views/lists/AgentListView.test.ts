import { expect, test, vi, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import {
	getByLabelText,
	render,
	screen,
	waitFor,
} from "@testing-library/svelte";
import AgentListView from "./AgentListView.svelte";
import { goto } from "$app/navigation";
import { listAgentsHandler } from "../../../mocks/handlers/agents";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("agent list view contains all registered agent names", async () => {
	const { getByRole } = render(AgentListView);
	const list = getByRole("list");

	await waitFor(() => {
		expect(list).toHaveTextContent("Cook");
		expect(list).toHaveTextContent("Researcher");
	});
});

test("agent list view create button routes to agent creation view", async () => {
	const user = userEvent.setup();
	const { getByLabelText } = render(AgentListView);
	const createButton = getByLabelText("Create agent");

	await user.click(createButton);

	expect(goto).toBeCalledWith("/agents/add");
});

test("clicking researcher detail button routes to researcher detail", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(AgentListView);
	const detailButton = await findByLabelText("Researcher agent detail");

	await user.click(detailButton);

	expect(goto).toBeCalledWith("/agents/2/edit");
});

test("agent list view can search for agents", async () => {
	const user = userEvent.setup();
	const { getByRole } = render(AgentListView);
	const search = getByRole("search");

	await user.click(search);
	await user.keyboard("Admin{Enter}");

	await waitFor(() => {
		expect(listAgentsHandler).toHaveBeenCalledTimes(2);
		expect((listAgentsHandler as Mock).mock.calls[1][0].request.url).toContain(
			"searchQuery=Admin",
		);
	});
});
