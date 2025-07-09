import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import LanguageModelToggle from "./LanguageModelToggle.svelte";
import { disableModelHandler, enableModelHandler } from "../../../mocks/handlers/models";

test('language model toggle shows name of given LLM', async () => {
    const { container } = render(LanguageModelToggle, {
        model: {
            id: 1,
            connectionId: 2,
            name: 'llama3.1:8b',
            enabled: false
        }
    });

    expect(container).toHaveTextContent("llama3.1:8b")
})

test('clicking model toggle of disabled model sends enable request', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(LanguageModelToggle, {
        model: {
            id: 3,
            connectionId: 2,
            name: 'llama3.1:8b',
            enabled: false
        }
    });

    const checkbox = getByRole('checkbox');
    await user.click(checkbox);

    expect(enableModelHandler).toBeCalled();
    expect((enableModelHandler as Mock).mock.calls[0][0].request.url).toContain('/api/models/3/enable');
})

test('clicking model toggle of enabled model sends disable request', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(LanguageModelToggle, {
        model: {
            id: 5,
            connectionId: 2,
            name: 'qwen2.5:3b',
            enabled: true
        }
    });

    const checkbox = getByRole('checkbox');
    await user.click(checkbox);

    expect(disableModelHandler).toBeCalled();
    expect((disableModelHandler as Mock).mock.calls[0][0].request.url).toContain('/api/models/5/disable');
})