import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ConnectionsList from "./ConnectionsList.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

test('connections list shows all LLM service connection names', async () => {
    const { container } = render(ConnectionsList);

    await waitFor(() => {
        expect(container).toHaveTextContent('Homelab');
    });
})

test('pressing add button in connections list routes to the connection create view', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ConnectionsList);
    
    const button = getByLabelText("Add connection");
    await user.click(button);

    expect(goto).toBeCalledWith("/admin/settings/connections/add")
})