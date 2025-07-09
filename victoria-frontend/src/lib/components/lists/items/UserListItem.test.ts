import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import type { UserListItem } from "$lib/types/user";
import ItemComponent from "./UserListItem.svelte"
import { goto } from "$app/navigation"

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

const testUser: UserListItem = {
    id: 3,
    username: "josh",
    role: 'user'
}

test('user list item shows name of given user', async () => {
    const { container } = render(ItemComponent, {
        user: testUser
    });

    expect(container).toHaveTextContent("josh");
})

test('user list item shows role of given user', async () => {
    const { container } = render(ItemComponent, {
        user: testUser
    });

    expect(container).toHaveTextContent("user");
})

test('pressing configure button in user list item routes to detail of given user', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ItemComponent, {
        user: testUser
    });

    const button = getByRole('button');
    await user.click(button);

    expect(goto).toBeCalledWith("/admin/users/3/edit")
})