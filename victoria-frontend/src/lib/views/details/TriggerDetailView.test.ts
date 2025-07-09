import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor, within } from '@testing-library/svelte';
import TriggerDetailView from './TriggerDetailView.svelte';
import { createTriggerHandler, deleteTriggerHandler, getTriggerHandler, updateTriggerHandler } from "../../../mocks/handlers/triggers";

test('trigger detail shows name, type, parameters and template of trigger', async () => {
    const { getByLabelText } = render(TriggerDetailView, {
        id: 2
    });
    
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });
    
    const nameBox = getByLabelText("Name") as HTMLInputElement;
    const typeDropdown = getByLabelText("Type");
    const urlBox = getByLabelText("URL") as HTMLInputElement;
    const intervalBox = getByLabelText("Interval") as HTMLInputElement;

    expect(nameBox.value).toBe("Retrieve news");
    expect(typeDropdown).toHaveTextContent("Poll");
    expect(urlBox.value).toBe("https://bbc.co.uk/rss");
    expect(intervalBox.value).toBe("200");
})

test('trigger detail can edit name of trigger', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 2
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });
    
    const nameBox = getByLabelText("Name") as HTMLInputElement;
    const saveButton = getByLabelText("Save trigger");

    await user.clear(nameBox);
    await user.type(nameBox, "Joshh");
    await user.click(saveButton);

    expect(updateTriggerHandler).toBeCalled();
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();

    expect(body).toHaveProperty('name', 'Joshh');
    expect(body).not.toHaveProperty('type');
})

test('trigger detail can edit template of trigger', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 2
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });
    
    const templateBox = getByLabelText("Template");
    const saveButton = getByLabelText("Save trigger");
    
    await user.clear(templateBox);
    await user.type(templateBox, "lolol");
    await user.click(saveButton);

    expect(updateTriggerHandler).toBeCalled();
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();

    expect(body).toHaveProperty('template', 'lolol');
    expect(body).not.toHaveProperty('name');
})

test('trigger detail can delete given trigger', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 3
    });

    // TODO: Spinners should be shown instead of fields and buttons when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });

    const deleteButton = getByLabelText("Delete trigger");

    await user.click(deleteButton);

    expect(deleteTriggerHandler).toBeCalled();
    expect((deleteTriggerHandler as Mock).mock.calls[0][0].request.url).toContain('/api/triggers/3');
})

test('trigger detail shows and can edit Poll trigger settings', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 2
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });

    const urlBox = getByLabelText("URL") as HTMLInputElement;
    const intervalBox = getByLabelText("Interval") as HTMLInputElement;
    const saveButton = getByLabelText("Save trigger");
    
    // Shows
    expect(urlBox.value).toBe("https://bbc.co.uk/rss");
    expect(intervalBox.value).toBe("200");

    // Edits
    await user.clear(urlBox);
    await user.type(urlBox, "https://seznam.cz");
    
    await user.clear(intervalBox);
    await user.type(intervalBox, "301");

    await user.click(saveButton);

    expect(updateTriggerHandler).toBeCalled();
    expect((updateTriggerHandler as Mock).mock.calls[0][0].request.url).toContain('/api/triggers/2');
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toMatchObject({
        settings: {
            interval: 301,
            url: "https://seznam.cz"
        }
    });
})

test('trigger detail shows and can edit Chat trigger settings', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 3
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });
    
    const receiverDropdown = getByLabelText("Chat receiver");
    const saveButton = getByLabelText("Save trigger");
    
    // Shows
    expect(receiverDropdown).toHaveTextContent('general');

    // Edits
    {
        const button = within(receiverDropdown).getByRole('button');
        await user.click(button);
        const option = within(receiverDropdown).getByLabelText('research');
        await user.click(option);
        
        await user.click(saveButton);
    }
    
    expect(updateTriggerHandler).toBeCalled();
    expect((updateTriggerHandler as Mock).mock.calls[0][0].request.url).toContain('/api/triggers/3');
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toMatchObject({
        settings: {
            receiver: 'research'
        }
    });
})

test('trigger detail shows and can edit Timer trigger settings', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 1
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });

    const intervalBox = getByLabelText("Interval") as HTMLInputElement;
    const saveButton = getByLabelText("Save trigger");
    
    // Shows
    expect(intervalBox.value).toBe("10");
    
    // Edits
    await user.clear(intervalBox);
    await user.type(intervalBox, "33");

    await user.click(saveButton);

    expect(updateTriggerHandler).toBeCalled();
    expect((updateTriggerHandler as Mock).mock.calls[0][0].request.url).toContain('/api/triggers/1');
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toMatchObject({
        settings: {
            interval: 33
        }
    });
})

test('trigger detail can change Poll trigger to Chat trigger', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: 2
    });
    
    // TODO: Spinners should be shown instead of fields when not loaded
    await waitFor(() => {
        expect(getTriggerHandler).toBeCalled();
    });
    
    { // Change type to chat
        const typeDropdown = getByLabelText("Type");
        const button = within(typeDropdown).getByRole('button');
        await user.click(button);
        const option = within(typeDropdown).getByLabelText('Chat');
        await user.click(option);
    }
    
    { // Set receiver
        const receiverDropdown = getByLabelText("Chat receiver");
        const button = within(receiverDropdown).getByRole('button');
        await user.click(button);
        const option = within(receiverDropdown).getByLabelText('research');
        await user.click(option);
    }    

    const saveButton = getByLabelText("Save trigger");
    await user.click(saveButton);
    
    expect(updateTriggerHandler).toBeCalled();
    expect((updateTriggerHandler as Mock).mock.calls[0][0].request.url).toContain('/api/triggers/2');
    let body = await (updateTriggerHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toMatchObject({
        settings: {
            type: 'chat',
            receiver: 'research'
        }
    });
})

test('trigger detail can create new trigger (given no id)', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(TriggerDetailView, {
        id: null
    });
    
    { // Name
        const nameBox = getByLabelText("Name") as HTMLInputElement;
        await user.type(nameBox, 'Retrieve car fuel level');
    }
    
    { // Type
        const typeDropdown = getByLabelText("Type");
        const button = within(typeDropdown).getByRole('button');
        await user.click(button);
        const option = within(typeDropdown).getByLabelText('Poll');
        await user.click(option);
    }
    
    { // URL
        const urlBox = getByLabelText("URL") as HTMLInputElement;
        await user.type(urlBox, 'http://spark:8000/fuel-level');
    }

    { // Interval
        const intervalBox = getByLabelText("Interval") as HTMLInputElement;
        await user.clear(intervalBox);
        await user.type(intervalBox, '20');
    }
    
    { // Template
        const templateBox = getByLabelText("Template");
        await user.clear(templateBox);
        await user.type(templateBox, "Car fuel level update: ${content}");
    }
    
    const createButton = getByLabelText("Create trigger");
    await user.click(createButton);

    
    expect(createTriggerHandler).toBeCalled();
    let body = await (createTriggerHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toMatchObject({
        name: 'Retrieve car fuel level',
        settings: {
            type: 'poll',
            interval: 20,
            url: 'http://spark:8000/fuel-level'
        },
        parser: "identity",
        template: "Car fuel level update: ${content}"
    });
})
