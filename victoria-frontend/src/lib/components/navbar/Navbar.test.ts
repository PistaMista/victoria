import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, within } from '@testing-library/svelte';
import Navbar from "./Navbar.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

test('can navigate to /myRoute via desktop navbar', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(Navbar, {
        routes: [
            {display_name: "My route", route_path: "/myRoute"}
        ]
    });
    
    const button = getByLabelText("My route");
    await user.click(button);

    expect(goto).toBeCalledWith("/myRoute");
})

test('clicking navbar expand button opens drawer with navigation buttons', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(Navbar, {
        routes: [
            {display_name: "My route", route_path: "/myRoute"}
        ]
    });
    
    const drawerButton = getByLabelText("Open navigation drawer");
    await user.click(drawerButton);
    
    const drawer = await findByLabelText("Navigation drawer");
    expect(drawer).toBeInTheDocument();
})

test('can navigate to /myRoute via mobile navbar', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(Navbar, {
        routes: [
            {display_name: "My route", route_path: "/myRoute"}
        ]
    });
    
    const drawerButton = getByLabelText("Open navigation drawer");
    await user.click(drawerButton);
    
    const drawer = await findByLabelText("Navigation drawer");
    const button = within(drawer).getByLabelText("My route");
    
    await user.click(button);
    
    expect(goto).toBeCalledWith("/myRoute");
})

