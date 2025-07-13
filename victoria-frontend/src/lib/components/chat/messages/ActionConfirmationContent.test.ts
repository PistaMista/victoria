import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { queryByLabelText, render, screen, waitFor } from '@testing-library/svelte';
import Component from "./ActionConfirmationContent.svelte";
import type { ActionConfirmationContent } from "$lib/types/message";
import { answerQueryHandler, getQueryAnswerHandler } from "../../../../mocks/handlers/queries";
import type { ActionInvocation } from "$lib/types/thought";

const invocation: ActionInvocation = {
    type: "ActionInvocation",
    name: "send_whatsapp_message",
    parameters: {
        recipient: "Someone",
        content: "Hello"
    }
};

const pendingContent: ActionConfirmationContent = {
    type: "action_confirmation",
    invocationThought: invocation,
    queryId: 3
};

const confirmedContent: ActionConfirmationContent = {
    type: "action_confirmation",
    invocationThought: invocation,
    queryId: 1
};

const abortedContent: ActionConfirmationContent = {
    type: "action_confirmation",
    invocationThought: invocation,
    queryId: 2
};

test('action confirmation message shows details of given invocation when pending', async () => {
    const { container } = render(Component, {
        content: pendingContent
    });

    await waitFor(() => {
        expect(container).toHaveTextContent("send_whatsapp_message");

        expect(container).toHaveTextContent("recipient");
        expect(container).toHaveTextContent("Someone");

        expect(container).toHaveTextContent("content");
        expect(container).toHaveTextContent("Hello");
    })
})

test('action confirmation message shows details of given invocation when confirmed', async () => {
    const { container } = render(Component, {
        content: confirmedContent
    });

    await waitFor(() => {
        expect(container).toHaveTextContent("send_whatsapp_message");

        expect(container).toHaveTextContent("recipient");
        expect(container).toHaveTextContent("Someone");

        expect(container).toHaveTextContent("content");
        expect(container).toHaveTextContent("Hello");
    })
})

test('action confirmation message shows details of given invocation when aborted', async () => {
    const { container } = render(Component, {
        content: abortedContent
    });

    await waitFor(() => {
        expect(container).toHaveTextContent("send_whatsapp_message");

        expect(container).toHaveTextContent("recipient");
        expect(container).toHaveTextContent("Someone");

        expect(container).toHaveTextContent("content");
        expect(container).toHaveTextContent("Hello");
    })
})

test('action confirmation message shows "confirmed" when query is already confirmed', async () => {
    const { container } = render(Component, {
        content: confirmedContent
    });
    
    await waitFor(() => {
        expect(container).toHaveTextContent("CONFIRMED");
    })
})

test('action confirmation message shows "aborted" when query is already aborted', async () => {
    const { container } = render(Component, {
        content: abortedContent
    });
    
    await waitFor(() => {
        expect(container).toHaveTextContent("ABORTED");
    })

})

test('pressing "execute" in action confirmation message sends "true" as a response to the invocation query', async () => {
    const user = userEvent.setup();
    const { findByLabelText } = render(Component, {
        content: pendingContent
    });
    
    const execute = await findByLabelText("Execute action");
    await user.click(execute);

    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toBe(true);
})

test('pressing "abort" in action confirmation message sends "false" as a response to the invocation query', async () => {
    const user = userEvent.setup();
    const { findByLabelText } = render(Component, {
        content: pendingContent
    });
    
    const abort = await findByLabelText("Abort action");
    await user.click(abort);

    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toBe(false);    
})

test('confirmation message buttons are hidden when confirmed', async () => {
    const { queryByLabelText } = render(Component, {
        content: confirmedContent
    });
    
    await waitFor(() => {
        expect(getQueryAnswerHandler).toBeCalled();
    })

    const execute = queryByLabelText("Execute action");
    const abort = queryByLabelText("Abort action");

    expect(execute).toBeNull();
    expect(abort).toBeNull();
})

test('confirmation message buttons are hidden when aborted', async () => {
    const { queryByLabelText } = render(Component, {
        content: abortedContent
    });

    await waitFor(() => {
        expect(getQueryAnswerHandler).toBeCalled();
    })

    const execute = queryByLabelText("Execute action");
    const abort = queryByLabelText("Abort action");

    expect(execute).toBeNull();
    expect(abort).toBeNull();
})