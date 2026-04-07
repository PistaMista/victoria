import { expect, test } from "vitest";
import { get } from 'svelte/store';
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import WebsocketStatusIndicator from "./WebsocketStatusIndicator.svelte";
import { connectWithRetry, disconnect, socketStatus } from "$lib/api/websocket";

test("websocket status indicator does not show message when socket connected", async () => {
	const { container } = render(WebsocketStatusIndicator);

	connectWithRetry();

	await waitFor(() => {
		expect(get(socketStatus).connected).toBe(true);
		expect(container).not.toHaveTextContent("Connection lost");
	});
});

test("websocket status indicator shows message when socket disconnects", async () => {
	const { container } = render(WebsocketStatusIndicator);

	connectWithRetry();

	await waitFor(() => {
		expect(get(socketStatus).connected).toBe(true);
	});

	disconnect();

	await waitFor(() => {
		expect(get(socketStatus).connected).toBe(false);
		expect(container).toHaveTextContent("Connection lost");
	});

	connectWithRetry(); // The default WS status in the test environment is CONNECTED
});

