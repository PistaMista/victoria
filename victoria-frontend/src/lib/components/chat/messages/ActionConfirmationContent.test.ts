import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import Component from "./ActionConfirmationContent.svelte";
import type { ActionConfirmationContent } from "$lib/types/message";
import { answerQueryHandler } from "../../../../mocks/handlers/queries";

const content: ActionConfirmationContent = {
    type: "action_confirmation",
    invocationThought: {
        type: "ActionInvocation",
        name: "send_whatsapp_message",
        parameters: {
            recipient: "Someone",
            content: "Hello"
        }
    },
    queryId: 2
};

test('action confirmation message shows details of given invocation', async () => {
    const { container } = render(Component, {
        content: content
    });

    expect(container).toHaveTextContent("send_whatsapp_message");

    expect(container).toHaveTextContent("recipient");
    expect(container).toHaveTextContent("Someone");

    expect(container).toHaveTextContent("content");
    expect(container).toHaveTextContent("Hello");
})

test('pressing "execute" in action confirmation message sends "true" as a response to the invocation query', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });
    
    const execute = getByLabelText("Execute action");
    await user.click(execute);

    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.body();
    expect(body).toBe(true);
})

test('pressing "abort" in action confirmation message sends "false" as a response to the invocation query', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });
    
    const abort = getByLabelText("Abort action");
    await user.click(abort);

    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.body();
    expect(body).toBe(false);    
})

test('confirmation message buttons are hidden after action is confirmed', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });

    const execute = getByLabelText("Execute action");
    const abort = getByLabelText("Abort action");

    await user.click(execute);

    expect(execute).not.toBeInTheDocument();
    expect(abort).not.toBeInTheDocument();
})

test('confirmation message buttons are hidden after action is aborted', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });

    const execute = getByLabelText("Execute action");
    const abort = getByLabelText("Abort action");

    await user.click(abort);

    expect(execute).not.toBeInTheDocument();
    expect(abort).not.toBeInTheDocument();
})