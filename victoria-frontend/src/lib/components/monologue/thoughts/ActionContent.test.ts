import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import ActionContent from "./ActionContent.svelte";
import type { ActionInvocation } from "$lib/types/thought";

const invocation: ActionInvocation = {
    type: "ActionInvocation",
    name: "lookup_in_table",
    parameters: {
        query: "Something or other",
        delay: 20,
        commit: true
    }
};

test('action thought content displays function name of taken action', async () => {
    const { container } = render(ActionContent, {
        content: invocation
    });

    expect(container).toHaveTextContent("lookup_in_table");
})

test('action thought content displays parameters of taken action (invocation of thought)', async () => {
    const { container } = render(ActionContent, {
        content: invocation
    });

    expect(container).toHaveTextContent('query: Something or other');
    expect(container).toHaveTextContent('delay: 20');
    expect(container).toHaveTextContent('commit: true');
})