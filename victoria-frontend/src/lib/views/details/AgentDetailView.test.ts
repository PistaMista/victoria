import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { findByLabelText, render, screen, waitFor, within } from '@testing-library/svelte';
import AgentDetailView from "./AgentDetailView.svelte";
import { createAgentHandler, deleteAgentHandler, getAgentHandler, updateAgentHandler } from "../../../mocks/handlers/agents";
import type { HTMLImageElement } from "happy-dom";

test('agent detail shows basic info about given agent', async () => {
    const { getByLabelText } = render(AgentDetailView, {
        id: 1
    });

    const nameBox = getByLabelText("Name") as HTMLInputElement;
    const modelDropdown = getByLabelText("Base model");
    const promptBox = getByLabelText("System prompt") as HTMLInputElement;
    const temperatureBox = getByLabelText("Temperature") as HTMLInputElement;
    const topKBox = getByLabelText("Top K") as HTMLInputElement;
    
    await waitFor(() => {
        expect(getAgentHandler).toBeCalled();
    })

    expect(nameBox.value).toBe("Cook");
    expect(modelDropdown).toHaveTextContent("gemma3:12b");
    expect(promptBox.value).toBe("You're a Cook that generates recipes for the week...");
    expect(temperatureBox.value).toBe("0.5");
    expect(topKBox.value).toBe("0.2");
})

test('agent detail can edit agent thumbnail', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(AgentDetailView, {
        id: 1
    });
    const newImage = new File(['lol'], 'image.png', { type: 'image/png' });
    
    const imagePicker = getByLabelText("Set agent thumbnail");
    await user.upload(imagePicker, newImage);
    
    const thumbnail = await findByLabelText("Agent thumbnail") as unknown as HTMLImageElement;
    expect(thumbnail.src).toBe("data:image/png;base64,bG9s");
    
    const saveButton = getByLabelText("Save agent");
    await user.click(saveButton);

    expect(updateAgentHandler).toBeCalled();
    let body = await (updateAgentHandler as Mock).mock.calls[0][0].request.json();

    expect(body).toMatchObject({
        thumbnailDataURI: "data:image/png;base64,bG9s"
    });
})

test('agent detail can edit given agent params', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(AgentDetailView, {
        id: 1
    });

    // FIXME: Fields should not be accessible unless data has finished loading
    await waitFor(() => {
        expect(getAgentHandler).toBeCalled();
    })

    // Name
    {
        const nameBox = getByLabelText("Name") as HTMLInputElement;
        await user.clear(nameBox);
        await user.type(nameBox, "John");
    }

    // Model
    {
        const modelDropdown = getByLabelText("Base model");
        const button = within(modelDropdown).getByRole('button');

        await user.click(button);

        const option = within(modelDropdown).getByLabelText('llama3.1:8b');
        await user.click(option);
    }


    // Temperature
    {
        const temperatureBox = getByLabelText("Temperature");
        await user.clear(temperatureBox);
        await user.click(temperatureBox);
        await user.keyboard("0.95{Enter}");
    }
    
    // Actions
    {
        const startMonologue = getByLabelText("Start monologue");
        await user.click(startMonologue);
    }

    const saveButton = getByLabelText("Save agent");
    await user.click(saveButton);

    expect(updateAgentHandler).toBeCalled();
    expect((updateAgentHandler as Mock).mock.calls[0][0].request.url).toContain("/api/agents/1");
    
    let body = await (updateAgentHandler as Mock).mock.calls[0][0].request.json();

    expect(body).not.toHaveProperty("systemPrompt");
    expect(body).not.toHaveProperty("modelParameters.top_k");
    expect(body).not.toHaveProperty("enabledTriggers");

    expect(body).toMatchObject({
        name: "John",
        baseModelId: 2,
        modelParameters: {
            temperature: 0.95
        },
        enabledActions: [1, 2, 3]
    });
})

test('agent detail can delete given agent', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(AgentDetailView, {
        id: 1
    });
    
    const button = getByLabelText("Delete agent");

    await user.click(button);

    expect(deleteAgentHandler).toBeCalled();
    expect((deleteAgentHandler as Mock).mock.calls[0][0].request.url).contain('/api/agents/1');
})

test('agent detail can create a new agent (with no id given)', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(AgentDetailView, {
        id: null
    });

    // Name
    {
        const nameBox = getByLabelText("Name") as HTMLInputElement;
        await user.clear(nameBox);
        await user.type(nameBox, "Victoria");
    }
    
    // Model
    {
        const modelDropdown = getByLabelText("Base model");
        const button = within(modelDropdown).getByRole('button');

        await user.click(button);

        const option = within(modelDropdown).getByLabelText('gemma3:12b');
        await user.click(option);
    }

    // Prompt
    {
        const promptBox = getByLabelText("System prompt");
        await user.clear(promptBox);
        await user.type(promptBox, "You do it all!");
    }


    // Temperature
    {
        const temperatureBox = getByLabelText("Temperature");
        await user.clear(temperatureBox);
        await user.click(temperatureBox);
        await user.keyboard("0.92{Enter}");        
    }
    
    // Triggers
    {
        const newsBox = getByLabelText("Check news");
        const discordBox = getByLabelText("Discord message received");
        await user.click(newsBox);
        await user.click(discordBox);
    }
    
    // Actions
    {
        const thinkBox = getByLabelText("Think");
        await user.click(thinkBox);
    }
    
    const createButton = getByLabelText("Create agent");

    await user.click(createButton);

    expect(createAgentHandler).toBeCalled();
    let body = await (createAgentHandler as Mock).mock.calls[0][0].request.json();
    expect(body).toMatchObject({
        name: "Victoria",
        baseModelId: 1,
        systemPrompt: "You do it all!",
        modelParameters: {
            temperature: 0.92,
            top_k: 40
        },
        enabledTriggers: [2, 4],
        enabledActions: [2]
    })
})
