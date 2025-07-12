import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import type { ChoicePromptContent } from "$lib/types/message";
import Component from "./ChoicePromptContent.svelte";
import { answerQueryHandler } from "../../../../mocks/handlers/queries";

const content: ChoicePromptContent = {
    type: "choice_prompt",
    queryId: 12,
    prompt: "Which color do you prefer?",
    choices: [
        {value: "blue"},
        {value: "red"},
        {value: true},
    ]
}

test('choice prompt shows all available options', async () => {
    const { container } = render(Component, {
        content: content
    });

    expect(container).toHaveTextContent("Which color do you prefer?");
    expect(container).toHaveTextContent("blue");
    expect(container).toHaveTextContent("red");
    expect(container).toHaveTextContent("true");
})

test('clicking on a choice in choice prompt sends that choice as a response to the invocation query', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });
    
    const redButton = getByLabelText("red");
    await user.click(redButton);
    
    expect(answerQueryHandler).toBeCalled();
    let body = await (answerQueryHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toBe("red");
})

test('choice prompt hides the choices after clicking a choice', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Component, {
        content: content
    });
    
    const blueButton = getByLabelText("blue");
    const redButton = getByLabelText("red");
    const trueButton = getByLabelText("true");

    await user.click(trueButton);
    
    expect(blueButton).not.toBeInTheDocument();
    expect(redButton).not.toBeInTheDocument();
    expect(trueButton).not.toBeInTheDocument();
})