import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import AbortButton from "./AbortButton.svelte";

test('abort button executes provided callback on click', async () => {
    const user = userEvent.setup();
    const callback = vi.fn();
    const { getByRole } = render(AbortButton,
        {
            onclick: callback
        }
    );

    const button = getByRole('button');
    await user.click(button);
    
    expect(callback).toBeCalled();
})