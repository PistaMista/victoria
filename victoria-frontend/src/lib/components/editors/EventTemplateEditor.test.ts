import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import EventTemplateEditor from "./EventTemplateEditor.svelte";

test('event template editor displays parser variables', async () => {
    const { container } = render(EventTemplateEditor, {
        variables: [ "content", "replyExchange" ],
        template: ""
    });

    expect(container).toHaveTextContent("$(content)");
    expect(container).toHaveTextContent("$(replyExchange)");
})

test('event template editor displays error when using undefined variable', async () => {
    const user = userEvent.setup();
    const { getByRole, container } = render(EventTemplateEditor, {
        variables: [ "content", "replyExchange" ],
        template: ""
    });
    
    const box = getByRole('textbox');
    
    await user.clear(box);
    await user.type(box, "Hehehe, undefined variable $(carrot)");
    
    expect(container).toHaveTextContent("Error: undefined variable 'carrot'");
})