import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { queryByLabelText, render, screen, waitFor } from '@testing-library/svelte';
import type { ChoicePromptContent } from "$lib/types/message";
import Component from "./ChoicePromptContent.svelte";
import { answerQueryHandler, getQueryAnswerHandler } from "../../../../mocks/handlers/queries";

const pendingQuery: ChoicePromptContent = {
    type: "choice_prompt",
    queryId: 3,
    prompt: "Which color do you prefer?",
    choices: [
        {value: "blue"},
        {value: "red"},
        {value: true},
    ]
}

const answeredQuery: ChoicePromptContent = {
    type: "choice_prompt",
    queryId: 5,
    prompt: "Which color do you prefer?",
    choices: [
        {value: "blue"},
        {value: "red"},
        {value: true},
    ]
}

test('choice prompt shows all available options for pending query', async () => {
    const { container } = render(Component, {
        content: pendingQuery
    });

    await waitFor(() => {
        expect(container).toHaveTextContent("Which color do you prefer?");
        expect(container).toHaveTextContent("blue");
        expect(container).toHaveTextContent("red");
        expect(container).toHaveTextContent("true");
    })
})

test('clicking on a choice in choice prompt sends that choice as a response to the pending query', async () => {
    const user = userEvent.setup();
    const { findByLabelText } = render(Component, {
        content: pendingQuery
    });
    
    const redButton = await findByLabelText("\"red\"");
    await user.click(redButton);
    
    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toBe("red");
})

test('choice prompt shows selected choice for answered query', async () => {
    const user = userEvent.setup();
    const { container } = render(Component, {
        content: answeredQuery
    });
    
    await waitFor(() => {
        expect(container).toHaveTextContent("Chosen: \"blue\"");
    })
})

test('choice prompt does not show choices for already answered query', async () => {
    const user = userEvent.setup();
    const { queryByLabelText } = render(Component, {
        content: answeredQuery
    });
    
    await waitFor(() => {
        expect(getQueryAnswerHandler).toBeCalled();
    })
    
    const blueButton = queryByLabelText("blue");
    const redButton = queryByLabelText("red");
    const trueButton = queryByLabelText("true");

    expect(blueButton).toBeNull();
    expect(redButton).toBeNull();
    expect(trueButton).toBeNull();
})