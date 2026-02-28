import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ChatReceiverDropdown from "./ChatReceiverDropdown.svelte";
import { listChatReceiversHandler } from "../../../mocks/handlers/chats";

// WARNING:
// Chat receivers are NOT an independent entity in the database - they are just a string
// property of chat triggers

test("chat receiver dropdown starts with first option selected", async () => {
	const { container } = render(ChatReceiverDropdown);

	await waitFor(() => {
		expect(listChatReceiversHandler).toBeCalled();
	});

	expect(container).toHaveTextContent("general");
	expect(container).not.toHaveTextContent("research");
});

test("chat receiver dropdown shows all chat receivers when clicked", async () => {
	const user = userEvent.setup();
	const { getByRole, container } = render(ChatReceiverDropdown);

	await waitFor(() => {
		expect(listChatReceiversHandler).toBeCalled();
	});

	const button = getByRole("button");
	await user.click(button);

	expect(container).toHaveTextContent("general");
	expect(container).toHaveTextContent("research");
});

test("chat receiver dropdown closes and shows option when it is selected", async () => {
	const user = userEvent.setup();
	const { getByRole, container, findByLabelText } =
		render(ChatReceiverDropdown);

	await waitFor(() => {
		expect(listChatReceiversHandler).toBeCalled();
	});

	const button = getByRole("button");
	await user.click(button);

	const option = await findByLabelText("research");
	await user.click(option);

	expect(option).not.toBeInTheDocument();
	expect(container).toHaveTextContent("research");
	expect(container).not.toHaveTextContent("general");
});
