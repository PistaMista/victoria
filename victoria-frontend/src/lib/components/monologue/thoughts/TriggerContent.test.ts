import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import TriggerContent from "./TriggerContent.svelte";
import type { TriggerInvocation } from "$lib/types/thought";
import { goto } from "$app/navigation";
import { getTriggerHandler } from "../../../../mocks/handlers/triggers";

vi.mock("$app/navigation", () => ({
    goto: vi.fn()
}))

const invocation: TriggerInvocation = {
    type: "TriggerInvocation",
    name: null,
    parameters: {
        eventId: 1
    }
};

test('trigger thought content displays name of trigger corresponding to the triggering event', async () => {
    const { container } = render(TriggerContent, {
        content: invocation
    });

    await waitFor(() => {
        expect(container).toHaveTextContent('Generate recipes');
    });
})

test('pressing trigger thought link routes to detail of triggering event', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerContent, {
        content: invocation
    });

    // TODO: The link should not be visible until all data finishes loading
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    })
    
    const link = getByLabelText("Go to triggering event");
    await user.click(link);

    expect(goto).toBeCalledWith("/events/1");
})