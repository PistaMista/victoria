import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ListViewHeaderButton from "./ListViewHeaderButton.svelte";

test('list view header button executes the provided callback', async () => {
    let callback = vi.fn(() => {});
    const user = userEvent.setup();
    const { getByRole } = render(ListViewHeaderButton, {
        onclick: callback
    });

    const button = getByRole('button');
    user.click(button);

    await waitFor(() => expect(callback).toBeCalled());
})