import { expect, test, vi, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ActionListView from "./ActionListView.svelte";
import { goto } from "$app/navigation";
import { listActionReposHandler } from "../../../mocks/handlers/action_repos";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

test('actions list view shows all registered action repositories', async () => {
    const { container } = render(ActionListView);

    await waitFor(() => {
        expect(container).toHaveTextContent("Home assistant tools");
        expect(container).toHaveTextContent("http://golem/PistaMista/HA-tools.git");
    })
})

test('clicking add button in actions list view routes to action repository add view', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ActionListView);
    const button = getByLabelText("Create action repository");

    await user.click(button);

    expect(goto).toBeCalledWith("/admin/actions/add");
})

test('actions list view can search for actions', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ActionListView);
    const searchBar = getByRole('search');

    await user.click(searchBar);
    await user.keyboard("Discord");

    await waitFor(() => {
        expect(listActionReposHandler).toBeCalledTimes(2);
        expect((listActionReposHandler as Mock).mock.calls[1][0].request.url).toContain("searchQuery=Discord")
    })
})