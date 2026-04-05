import { expect, test, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/svelte";
import Subscriber from "./Subscriber.svelte";
import SubscriberTestbed from "./SubscriberTestbed.svelte";
import type { TestSubscription } from "$lib/types/websocket";
import { connectWithRetry, disconnect } from "$lib/api/websocket";
import { connectionHandler, disconnectionHandler } from "../../../mocks/handlers/websocket";

test("subscriber shows connecting message when subscribing", async () => {
	connectWithRetry();
	await waitFor(() => {
		expect(connectionHandler).toHaveBeenCalled();
	});

	const sub: TestSubscription = { type: "test", declineRequest: false };
	const { container } = render(Subscriber, {
		subscription: sub,
		handler: () => { }
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Connecting...");
		expect(container).not.toHaveTextContent("CHILD");
	});

	disconnect();
	await waitFor(() => {
		expect(disconnectionHandler).toHaveBeenCalled();
	});
});

test("subscriber shows disconnected message when cancelled", async () => {
	connectWithRetry();
	await waitFor(() => {
		expect(connectionHandler).toHaveBeenCalled();
	});

	const sub: TestSubscription = { type: "test", declineRequest: true };
	const { container } = render(Subscriber, {
		subscription: sub,
		handler: () => { }
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Disconnected.");
		expect(container).toHaveTextContent("TEST REFUSE");
	});

	disconnect();
	await waitFor(() => {
		expect(disconnectionHandler).toHaveBeenCalled();
	});
});


test("subscriber shows children when subscribed", async () => {
	connectWithRetry();
	await waitFor(() => {
		expect(connectionHandler).toHaveBeenCalled();
	});

	const { container } = render(SubscriberTestbed);

	await waitFor(() => {
		expect(container).toHaveTextContent("CHILD");
		expect(container).not.toHaveTextContent("Connecting");
		expect(container).not.toHaveTextContent("Disconnecting");
		expect(container).not.toHaveTextContent("Disconnected");
	});

	disconnect();
	await waitFor(() => {
		expect(disconnectionHandler).toHaveBeenCalled();
	});
});

test("subscriber calls handler when receiving message", async () => {
	connectWithRetry();
	await waitFor(() => {
		expect(connectionHandler).toHaveBeenCalled();
	});

	let sub1count = 0;
	let sub2count = 0;
	let sub1correct = false;
	let sub2correct = false;

	render(Subscriber, {
		subscription: { type: "test", declineRequest: false, replyWith: 42 },
		handler: (msg: any) => { sub1count++; sub1correct = (msg === 42); }
	});
	render(Subscriber, {
		subscription: { type: "test", declineRequest: false, replyWith: 69 },
		handler: (msg: any) => { sub2count++; sub2correct = (msg === 69); }
	});

	await waitFor(() => {
		expect(sub1count).toBe(1);
		expect(sub2count).toBe(1);
		expect(sub1correct).toBeTruthy();
		expect(sub2correct).toBeTruthy();
	});

	disconnect();
	await waitFor(() => {
		expect(disconnectionHandler).toHaveBeenCalled();
	});
});
