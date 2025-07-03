import { expect, test, assert, type Mock, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, waitFor, within } from '@testing-library/svelte';
import ChatListView from "./ChatListView.svelte";
import { chatCreateHandler, listChatsHandler } from "../../../mocks/handlers/chats";
import { goto } from '$app/navigation';

vi.mock('$app/navigation', () => ({
    goto: vi.fn()
}))

test('chat list view contains all chat titles from API response', async () => {
    const { getByRole } = render(ChatListView);
    const list = getByRole('list');

    await waitFor(() => {
        expect(listChatsHandler).toBeCalled();
        
        // The default sortBy mode is 'recent'
        expect((listChatsHandler as Mock).mock.calls[0][0].request.url).toContain("sortBy=recent");
    });
    
    expect(list).toHaveTextContent("System admin");
    expect(list).toHaveTextContent("Language learning");
})

test('chat list view sends request to create new chat', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatListView);
    const createButton = getByLabelText("Create chat");

    
    // Click the button
    await user.click(createButton);

    // Creation request should be sent
    expect(chatCreateHandler).toBeCalled()
})

test('chat list view routes to new chat after creation', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatListView);
    const createButton = getByLabelText("Create chat");

    // Click the button
    await user.click(createButton);

    expect(goto).toBeCalledWith("/chats/3")
});

test('chat list view can sort by importance', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");
    const button = within(sortByDropdown).getByRole('button');

    // Click the dropdown
    await user.click(button);

    const importanceOption = await findByLabelText("Importance");
    
    // Select importance option
    await user.click(importanceOption);

    // Appropriate request should be sent
    expect(listChatsHandler).toBeCalledTimes(2);
    expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=importance');
})

test('chat list view can sort by recent', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");
    const button = within(sortByDropdown).getByRole('button');

    // Click the dropdown
    await user.click(button);

    const recentOption = await findByLabelText("Recent");
    
    // Select recent option
    await user.click(recentOption);
    
    // Appropriate request should be sent
    expect(listChatsHandler).toBeCalledTimes(2);
    expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=recent');
})

test('chat list view can sort by length', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");
    const button = within(sortByDropdown).getByRole('button');

    // Click the dropdown
    await user.click(button);

    const lengthOption = await findByLabelText("Length");
    
    // Select length option
    await user.click(lengthOption);
    
    // Appropriate request should be sent
    expect(listChatsHandler).toBeCalledTimes(2);
    expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=length');
})

test('chat list view can filter by chat receiver', async () => {
    const user = userEvent.setup();
    const { getByLabelText, findByLabelText } = render(ChatListView);

    const filterByDropdown = getByLabelText("Filter by chat receiver");
    const button = within(filterByDropdown).getByRole('button');
    
    // Click the chat receiver dropdown
    await user.click(button);
    
    const generalOption = await findByLabelText("general");

    // Select the 'general' option
    await user.click(generalOption);

    // Appropriate request should be sent
    expect(listChatsHandler).toBeCalledTimes(2);
    expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('receiver=general');
})

test('chat list view can search for chats', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ChatListView);

    const searchBar = getByRole('search');
    
    // No search query by default
    await waitFor(() => {
        expect(listChatsHandler).toHaveBeenCalledOnce();
        expect((listChatsHandler as Mock).mock.calls[0][0].request.url).not.toContain('searchQuery=');
    });

    // Type a search query
    user.type(searchBar, "pineapples");
    
    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalledTimes(2);
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('searchQuery=pineapples')
    })
})