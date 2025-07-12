import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import ExchangeContextButton from "./ExchangeContextButton.svelte";

test.todo('exchange context button executes the provided callback', async () => {
    const user = userEvent.setup();
    const callback = vi.fn();
    const { getByRole } = render(ExchangeContextButton,
        {
            onclick: callback
        }
    );

    const button = getByRole('button');
    await user.click(button);
    
    expect(callback).toBeCalled();
})