import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, waitFor } from "@testing-library/svelte";
import ChatWindow from "./ChatWindow.svelte";
import { getExchangesHandler } from "../../../mocks/handlers/chats";

test("chat window gradually loads exchanges", async () => {
	const { container } = render(ChatWindow, {
		id: 1,
	});

	expect(getExchangesHandler).not.toBeCalled();

	await waitFor(() => {
		// Expect the user messages to show up
		expect(container).toHaveTextContent("Hmmm, yeees");
		expect(container).toHaveTextContent("Hello?");
		expect(container).not.toHaveTextContent("Goodbye.");
	});

	await waitFor(() => {
		// Expect the user messages to show up
		expect(container).toHaveTextContent("Hmmm, yeees");
		expect(container).toHaveTextContent("Hello?");
		expect(container).toHaveTextContent("Goodbye.");
	});
});

test("chat window should send poll requests repeatedly", async () => {
	render(ChatWindow, {
		id: 1,
	});

	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(1);
		expect(
			(getExchangesHandler as Mock).mock.calls[0][0].request.url,
		).toContain("?after=0");
	});
	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(2);
		expect(
			(getExchangesHandler as Mock).mock.calls[1][0].request.url,
		).toContain("?after=2700");
	});
	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(3);
		expect(
			(getExchangesHandler as Mock).mock.calls[2][0].request.url,
		).toContain("?after=3300");
	});
	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(4);
		expect(
			(getExchangesHandler as Mock).mock.calls[3][0].request.url,
		).toContain("?after=3300");
	});
	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(5);
		expect(
			(getExchangesHandler as Mock).mock.calls[4][0].request.url,
		).toContain("?after=3300");
	});
	await waitFor(() => {
		expect(getExchangesHandler).toBeCalledTimes(6);
		expect(
			(getExchangesHandler as Mock).mock.calls[5][0].request.url,
		).toContain("?after=3300");
	});
});
