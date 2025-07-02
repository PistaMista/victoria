import { expect, test, assert, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, waitFor } from '@testing-library/svelte';
import ChatListView from "./ChatListView.svelte";
import { chatCreateHandler, listChatsHandler } from "../../../mocks/handlers/chats";

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
    user.click(createButton);

    // Creation request should be sent
    await waitFor(() => 
        expect(chatCreateHandler).toBeCalled()
    );
})

test('chat list view routes to new chat after creation', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(ChatListView);
    const createButton = getByLabelText("Create chat");

    // Click the button
    user.click(createButton);

    await waitFor(() => {
        expect(window.location.pathname).toBe("/chats/3")
    });
});

test('chat list view can sort by importance', async () => {
    const user = userEvent.setup();
    const { getByLabelText, getByRole } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");

    // Click the dropdown
    user.click(sortByDropdown);

    const importanceOption = getByLabelText("Importance");
    
    // Select importance option
    user.click(importanceOption);

    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalled();
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=importance');
    })
})

test('chat list view can sort by recent', async () => {
    const user = userEvent.setup();
    const { getByLabelText, getByRole } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");

    // Click the dropdown
    user.click(sortByDropdown);

    const recentOption = getByLabelText("Recent");
    
    // Select recent option
    user.click(recentOption);
    
    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalledTimes(2);
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=recent');
    })
})

test('chat list view can sort by length', async () => {
    const user = userEvent.setup();
    const { getByLabelText, getByRole } = render(ChatListView);
    
    const sortByDropdown = getByLabelText("Sort by");

    // Click the dropdown
    user.click(sortByDropdown);

    const lengthOption = getByLabelText("Length");
    
    // Select length option
    user.click(lengthOption);
    
    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalledTimes(2);
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('sortBy=length');
    })
})

test('chat list view can filter by chat receiver', async () => {
    const user = userEvent.setup();
    const { getByLabelText, getByRole } = render(ChatListView);

    const filterByDropdown = getByLabelText("Filter by chat receiver");
    
    // Click the chat receiver dropdown
    user.click(filterByDropdown);
    
    const generalOption = getByLabelText("general");

    // Select the 'general' option
    user.click(generalOption);

    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalledTimes(2);
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('receiver=general');
    })
})

test('chat list view can search for chats', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ChatListView);

    const searchBar = getByRole('search');

    // Type a search query
    user.type(searchBar, "pineapples");
    
    // Appropriate request should be sent
    await waitFor(() => {
        expect(listChatsHandler).toBeCalledTimes(2);
        expect((listChatsHandler as Mock).mock.calls[1][0].request.url).toContain('searchQuery=pineapples')
    })
})