import { expect, test, assert } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import AssistantMessage from "./AssistantMessage.svelte";

test('AssistantMessage displays given message', async () => {
    render(AssistantMessage, {
        content: "Hello, this is a message!",
        delete_action: () => {}
    });

    var content = screen.getByRole("article");
    expect(content).toHaveTextContent("Hello, this is a message!");
});

test('execute AssistantMessage delete action', async () => {
    assert.fail("not implemented")
})