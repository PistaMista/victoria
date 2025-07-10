import { expect, test, type Mock, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ChatPrompt from "./ChatPrompt.svelte";
import { getChatOptionsHandler, sendMessageHandler } from "../../../mocks/handlers/chats";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

test('chat prompt send button does not send message when clicked with an empty prompt', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatPrompt, {
        id: 1
    });
    
    const sendButton = getByLabelText("Send message");
    await user.click(sendButton);

    expect(sendMessageHandler).not.toBeCalled();
    
})

test('chat prompt can send text message to the conversation with given id', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatPrompt, {
        id: 1
    });
    
    const messageBox = getByLabelText("Message box");
    const sendButton = getByLabelText("Send message");
    
    await user.type(messageBox, "Hello there!");
    await user.click(sendButton);

    expect(sendMessageHandler).toBeCalled();
    let body = await (sendMessageHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toMatchObject({
        message: "Hello there!"
    });
})

test('chat prompt options button routes to options of conversation with given id', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatPrompt, {
        id: 1
    });
    
    const optionsButton = getByLabelText("Show chat options");
    await user.click(optionsButton);

    expect(goto).toBeCalledWith("/chats/1/options");
})