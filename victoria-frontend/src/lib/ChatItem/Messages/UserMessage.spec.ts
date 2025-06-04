import UserMessage from "./UserMessage.svelte";
import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

test('UserMessage displays given message', async () => {
    render(UserMessage, {
        content: "Hello, this is a message!",
        delete_action: () => {}
    });

    var content = screen.getByRole("article");
    expect(content).toHaveTextContent("Hello, this is a message!");
});

test('edit UserMessage', async () => {
    const user = userEvent.setup();
    render(UserMessage, { 
        content: "Hello!", 
        delete_action: () => {}
    });
    
    var content = screen.getByRole("article");
    expect(content).toHaveTextContent("Hello!");
    
    // Hovering over the content opens the context menu
    await user.hover(content);

    // The first context action starts editing the message...
    const edit_button = screen.getAllByRole("button")[0];
    await user.click(edit_button);
    
    const text_area = screen.getByRole("textbox");

    // ...user edits the message...
    await user.type(text_area, "Goodbye");
    
    // ...editing stops when the user clicks off the element.
    await user.click(document.body);

    content = screen.getByRole("article");
    expect(content).toHaveTextContent("Goodbye");
})