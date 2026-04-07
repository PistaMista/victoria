import { expect, test, vi, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import { goto } from "$app/navigation";
import Component from "./ExchangeMonologue.svelte";
import { connectWithRetry, disconnect } from "$lib/api/websocket";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("exchange monologue shows title of monologue", async () => {
	connectWithRetry();

	const { container } = render(Component, {
		monologueId: 1
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Research thesis ideas");
	});

	disconnect();
});

test("exchange monologue clicking title of monologue routes to monologue detail", async () => {
	connectWithRetry();

	const user = userEvent.setup();
	const { findAllByLabelText } = render(Component, {
		monologueId: 2
	});

	const buttons = await findAllByLabelText("Go to monologue");

	await user.click(buttons[0]);
	expect(goto).toBeCalledWith("/monologues/2");

	disconnect();
});
