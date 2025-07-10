<script lang="ts">
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import ListViewHeaderDropdown, { type Option } from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
    import ChatListItem from "$lib/components/lists/items/ChatListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import { getCurrentUserChats, createNewChat, type SortMode, getChatReceivers } from "$lib/api/chatting";
    import type { Chat } from "$lib/types/chat"
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    
    let chats: Chat[] = [];
    let receivers: string[] = [];
    let sortByOption: Option | null;
    let receiverOption: Option | null;
    let searchQuery: string = "";
    let mounted = false;
    
    async function openNewChat() {
        let { id } = await createNewChat();
        let stringId = id.toString();
        goto(`/chats/${stringId}`);
    }
    
    function searchSubmit(val: string) {
        alert(val);
    }

    onMount(async () => {
        mounted = true;
        receivers = await getChatReceivers();
    });

    $: if (mounted) {
        (async () => {
            let receiver: string | null = receiverOption?.value;
            let query: string | null = searchQuery ? searchQuery : null;
            let sortBy: SortMode = sortByOption?.value ?? 'recent';        
            chats = await getCurrentUserChats(sortBy, receiver, query);
        })();
    }
</script>

<ListView>
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar
            ontype={(val) => {searchQuery = val}}
        />
        <div class="mx-2 content-center flex flex-row">
            <!-- Sort by Recent/Longest/Important -->
            <ListViewHeaderDropdown 
                title="Sort" 
                aria-label="Sort by" 
                options={[
                    {displayName: "Recent", ariaLabel: "Recent", value: 'recent'},
                    {displayName: "Longest", ariaLabel: "Length", value: 'length'},
                    {displayName: "Importance", ariaLabel: "Importance", value: 'importance'}
                ]}
                bind:chosenOption={sortByOption}
            />
            <!-- Filter by chat receiver -->
            <ListViewHeaderDropdown 
                title="Receiver" 
                aria-label="Filter by chat receiver" 
                options={
                [
                    {displayName: "any", ariaLabel: "any", value: null},
                    ...receivers.map(name => ({
                        displayName: name, ariaLabel: name, value: name
                    }))
                ]
                }
                bind:chosenOption={receiverOption}
            />

            <ListViewHeaderButton onclick={openNewChat} aria-label="Create chat"><PlusOutline class="w-6 h-6"/></ListViewHeaderButton>
        </div>
    </svelte:fragment>

    
    <svelte:fragment slot="items">
        {#each chats as chat}
            <ChatListItem {chat}/>
        {/each}
    </svelte:fragment>
</ListView>