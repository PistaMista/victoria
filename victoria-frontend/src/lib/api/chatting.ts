import type { Chat } from "$lib/types/chat";
import { Chat as ChatSchema } from "$lib/types/chat";
import { z } from "zod";

export type SortMode = 'recent' | 'length' | 'importance';

export async function getCurrentUserChats(sortBy: SortMode = 'recent', receiver: string | null = null, searchQuery: string | null = null): Promise<Chat[]> {
    const params = new URLSearchParams({
        sortBy: sortBy
    });
    
    if (receiver) {
        params.append("receiver", receiver);
    }
    
    if (searchQuery) {
        params.append("searchQuery", searchQuery);
    }

    const res = await fetch(`/api/chats?${params.toString()}`, { 
        method: 'GET' 
    });
    const json = await res.json();
    return z.array(ChatSchema).parse(json);
}

export async function getChatReceivers(): Promise<string[]> {
    const res = await fetch('/api/chats/receivers', {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(z.string()).parse(json);
}

export async function createNewChat(): Promise<Chat> {
    const res = await fetch('/api/chats', { method: 'POST' });
    const json = await res.json();
    return ChatSchema.parse(json);
}