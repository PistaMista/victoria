<script lang="ts">
    import { getChatReceivers } from "$lib/api/chatting";
    import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    import Loader from "../placeholders/Loader.svelte";
    
    export let chosenReceiver: string | null = null;

    let receivers: string[] = [];
    let dropdownOpen: boolean = false;
    
    let dataPromise: Promise<any> = Promise.resolve();
    
    async function load() {
        receivers = await getChatReceivers();
        chosenReceiver = receivers.at(0) ?? null;
    }

    onMount(() => {
        dataPromise = load()
    })
</script>

<Loader
    promise={dataPromise}
    pendingMessage="Loading valid chat receivers..."
    rejectMessage="Failed to load chat receivers"
>
<div {...$$restProps}>
    <Button class="flex flex-row w-full">{chosenReceiver ?? "Choose receiver..."}<ChevronDownOutline class="w-6 h-6"/></Button>
    <Dropdown bind:open={dropdownOpen}>
        {#each receivers as receiver}
            <DropdownItem
                aria-label={receiver}
                on:click={() => {
                    chosenReceiver = receiver;
                    dropdownOpen = false;
                }}
            >
                {receiver}
            </DropdownItem>
        {/each}
    </Dropdown>
</div>
</Loader>