import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { getByLabelText, render, screen, waitFor } from '@testing-library/svelte';
import MonologueDetailView from "./MonologueDetailView.svelte";
import { abortMonologueHandler, getMonologueHandler } from "../../../mocks/handlers/monologues";

test('monologue detail view shows summary and title of given monologue', async () => {
    const { container } = render(MonologueDetailView, {
        id: 1
    });

    await waitFor(() => {
        // Summary
        expect(container).toHaveTextContent("Searching the web for sources");
        // Title
        expect(container).toHaveTextContent("Research thesis ideas");
    });
})

test('monologue detail allows aborting given monologue', async () => {
    const user = userEvent.setup();
    const { findByLabelText } = render(MonologueDetailView, {
        id: 2
    });

    const abortButton = await findByLabelText("Abort monologue");

    await user.click(abortButton);

    expect(abortMonologueHandler).toBeCalled();
    expect((abortMonologueHandler as Mock).mock.calls[0][0].request.url).toContain('/api/monologues/2/abort');
})

// Rest is covered by tests for ThoughtTimeline, MonologueStatusIndicator and AgentCard