import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import NavbarItem from "./NavbarItem.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

test('clicking navbar item routes to the provided route', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(NavbarItem, {
        route: {display_name: "Route", route_path: "/lolol"}
    });
    
    const button = getByRole('link');
    await user.click(button);

    expect(goto).toBeCalledWith("/lolol");
})