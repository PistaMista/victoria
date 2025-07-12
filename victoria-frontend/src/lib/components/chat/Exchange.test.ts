import { expect, test, vi, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import type { Exchange } from "$lib/types/exchange";
import { goto } from "$app/navigation";
import Component from "./Exchange.svelte";
import { duplicateChatHandler } from "../../../mocks/handlers/chats";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

const testExchange: Exchange = {
    id: 2,
    chatId: 3,
    timestamp: 2500,
    userMessage: {
        id: 2,
        timestamp: 2405,
        content: {
            type: 'markdown',
            markdownText: "My user message"
        }
    },
    monologueIds: [1, 2]
};

const userMessageNullExchange: Exchange = {
    id: 2,
    chatId: 3,
    timestamp: 2500,
    userMessage: null,
    monologueIds: [1, 2]
};

test('exchange shows user message of given exchange', async () => {
    const { container } = render(Component, {
        exchange: testExchange
    });

    expect(container).toHaveTextContent("My user message");
})

test('exchange shows all text from agent messages of given exchange', async () => {
    const { container } = render(Component, {
        exchange: testExchange
    });
    
    await waitFor(() => {
        expect(container).toHaveTextContent("Agent message!");
        expect(container).toHaveTextContent("Pick a thing");
        expect(container).toHaveTextContent("Are you sure you wish to do this?");
    })
})

test('clicking name of monologue at the bottom of exchange routes to the monologue detail', async () => {
    const user = userEvent.setup();
    const { findAllByLabelText } = render(Component, {
        exchange: testExchange
    });
    
    const buttons = await findAllByLabelText("Go to monologue");

    await user.click(buttons[0]);
    expect(goto).toBeCalledWith("/monologues/1");

    await user.click(buttons[1]);
    expect(goto).toBeCalledWith("/monologues/2");
})

test('clicking "new chat from here" button sends request to duplicate current chat', async () => {
    const user = userEvent.setup();
    const { findByLabelText } = render(Component, {
        exchange: testExchange
    });
    
    const button = await findByLabelText("Create new chat from here");
    await user.click(button);

    expect(duplicateChatHandler).toBeCalled();
    expect((duplicateChatHandler as Mock).mock.calls[0][0].request.url).toContain("/chats/3/duplicate");

    let body = await (duplicateChatHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toHaveProperty('toExchange', 2);
})

test('exchange can have user message set to null (if initiated by the agent)', async () => {
    expect(() => render(Component, {
        exchange: userMessageNullExchange    
    })).not.toThrow();
})