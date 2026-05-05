import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, waitFor, within } from "@testing-library/svelte";
import ChatOptionsView from "./ChatOptionsView.svelte";
import {
	chatDeleteHandler,
	getChatOptionsHandler,
	listChatReceiversHandler,
	setChatOptionsHandler,
} from "../../../mocks/handlers/chats";

test("chat options view allows setting chat receiver of given chat", async () => {
	const user = userEvent.setup();
	const { getByLabelText, findByLabelText } = render(ChatOptionsView, {
		id: 1,
	});

	await waitFor(() => {
		expect(getChatOptionsHandler).toBeCalled();
		expect(listChatReceiversHandler).toBeCalled();
	});

	{
		// Select chat receiver
		const dropdown = getByLabelText("Select chat receiver");
		const button = within(dropdown).getByRole("button");
		await user.click(button);

		const option = await findByLabelText("research");
		await user.click(option);
	}

	{
		// Save
		const button = getByLabelText("Save chat options");
		await user.click(button);
	}

	expect(setChatOptionsHandler).toBeCalled();
	let body = await (
		setChatOptionsHandler as Mock
	).mock.calls[0][0].request.json();
	expect(body).toHaveProperty("receiver", "research");
	expect(body).not.toHaveProperty("enabledActionIds");
});

test("chat options view allows editing allowed actions taken by agents receiving user messages", async () => {
	const user = userEvent.setup();
	const { getByLabelText } = render(ChatOptionsView, {
		id: 1,
	});

	await waitFor(() => {
		expect(getChatOptionsHandler).toBeCalled();
	});

	{
		// Edit actions
		const calendar = getByLabelText("Add to calendar");
		const think = getByLabelText("Think");

		await user.click(calendar);
		await user.click(think);
	}

	{
		// Save
		const button = getByLabelText("Save chat options");
		await user.click(button);
	}

	expect(setChatOptionsHandler).toBeCalled();
	let body = await (
		setChatOptionsHandler as Mock
	).mock.calls[0][0].request.json();
	expect(body).not.toHaveProperty("receiver");
	expect(body).toHaveProperty("enabledActionIds", [2, 3]);
});

test("chat options view allows deleting given chat", async () => {
	const user = userEvent.setup();
	const { getByLabelText } = render(ChatOptionsView, {
		id: 1,
	});

	await waitFor(() => {
		expect(getChatOptionsHandler).toBeCalled();
	});

	const button = getByLabelText("Delete chat");
	await user.click(button);
	const confirmButton = getByLabelText("Delete");
	await user.click(confirmButton);

	expect(chatDeleteHandler).toBeCalled();
	expect((chatDeleteHandler as Mock).mock.calls[0][0].request.url).toContain(
		"/api/chats/1",
	);
});
