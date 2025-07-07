import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import { goto } from "$app/navigation";
import type { TriggerListItem } from "$lib/types/trigger";
import Component from "./TriggerListItem.svelte";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

const testTrigger: TriggerListItem = {
    id: 3,
    name: "General chat",
    type: "chat"
};

test('trigger list item shows name of given trigger', async () => {
    const { container } = render(Component, {
        trigger: testTrigger
    });

    expect(container).toHaveTextContent("General chat");
})

test('trigger list item shows type of given trigger', async () => {
    const { container } = render(Component, {
        trigger: testTrigger
    });

    expect(container).toHaveTextContent("CHAT");
})

test('clicking trigger list item routes to detail of given trigger', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(Component, {
        trigger: testTrigger
    });
    const button = getByRole('button');

    await user.click(button);

    expect(goto).toBeCalledWith("/admin/triggers/3");
})